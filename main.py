from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from database import init_db
from memory import MemoryManager
from rag import RAGKnowledgeBase
from llm import GeminiLLM
from agent import HelpdeskAgent


# ==================================================
# PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"


# ==================================================
# FASTAPI APPLICATION
# ==================================================

app = FastAPI(
    title="AI IT Helpdesk & Troubleshooting Agent",
    description=(
        "An AI-powered helpdesk using Gemini, "
        "conversation memory, RAG, and agent tools."
    ),
    version="1.0.0"
)


# ==================================================
# CORS
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ==================================================
# STATIC FILES
# ==================================================

if not STATIC_DIR.is_dir():
    raise RuntimeError(
        f"Static folder not found: {STATIC_DIR}"
    )

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)


# ==================================================
# INITIALIZE COMPONENTS
# ==================================================

init_db()

memory = MemoryManager()

rag = RAGKnowledgeBase(
    str(KNOWLEDGE_BASE_DIR)
)

llm = GeminiLLM()

agent = HelpdeskAgent(llm)


# ==================================================
# REQUEST MODEL
# ==================================================

class ChatRequest(BaseModel):
    user_id: str = "EMP001"
    message: str


# ==================================================
# HOME PAGE
# ==================================================

@app.get("/", response_class=HTMLResponse)
async def home():
    html_file = TEMPLATES_DIR / "index.html"

    if not html_file.is_file():
        raise HTTPException(
            status_code=500,
            detail=f"HTML file not found: {html_file}"
        )

    return HTMLResponse(
        content=html_file.read_text(encoding="utf-8")
    )


# ==================================================
# HEALTH CHECK
# ==================================================

@app.get("/health")
async def health():
    return {
        "project": "AI IT Helpdesk & Troubleshooting Agent",
        "status": "running"
    }


# ==================================================
# CHAT ENDPOINT
# ==================================================

@app.post("/chat")
def chat(request: ChatRequest):

    user_id = request.user_id.strip()
    user_message = request.message.strip()

    if not user_id:
        raise HTTPException(
            status_code=400,
            detail="User ID cannot be empty."
        )

    if not user_message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    try:
        # ==========================================
        # STEP 1: SAVE USER MESSAGE
        # ==========================================

        memory.remember_message(
            user_id,
            "user",
            user_message
        )

        # ==========================================
        # STEP 2: FIRST LLM
        # UNDERSTAND THE USER QUERY
        # ==========================================

        understanding = llm.understand_query(
            user_message
        )

        # ==========================================
        # STEP 3: RETRIEVE MEMORY
        # ==========================================

        recent = memory.get_context(user_id)

        long_term = memory.get_long_term_memory(
            user_id
        )

        memory_context = (
            "RECENT CONVERSATION:\n"
            + "\n".join(
                f"{item['role']}: {item['message']}"
                for item in recent
            )
            + "\n\nLONG-TERM MEMORY:\n"
            + "\n".join(
                item["memory"]
                for item in long_term
            )
        )

        # ==========================================
        # STEP 4: RAG SEARCH
        # ==========================================

        rag_results = rag.search(
            user_message,
            top_k=4
        )

        rag_context = "\n\n".join(
            (
                f"[Source: {item['source']}\n"
                f"Score: {item['score']:.3f}]\n\n"
                f"{item['text']}"
            )
            for item in rag_results
        )

        if not rag_context:
            rag_context = (
                "No relevant company document was found."
            )

        # ==========================================
        # STEP 5: AGENT AND TOOLS
        # ==========================================

        decision, tool_result = agent.run(
            user_id=user_id,
            user_message=user_message,
            understanding=understanding,
            memory_context=memory_context,
            rag_context=rag_context
        )

        # ==========================================
        # STEP 6: FINAL LLM RESPONSE
        # ==========================================

        answer = llm.final_response(
            user_message=user_message,
            memory_context=memory_context,
            rag_context=rag_context,
            agent_decision=decision,
            tool_result=tool_result
        )

        # ==========================================
        # STEP 7: SAVE ASSISTANT RESPONSE
        # ==========================================

        memory.remember_message(
            user_id,
            "assistant",
            answer
        )

        # ==========================================
        # STEP 8: LONG-TERM MEMORY
        # ==========================================

        memory_triggers = [
            "my laptop",
            "my computer",
            "my device",
            "i use windows",
            "i work in",
            "my department"
        ]

        if any(
            phrase in user_message.lower()
            for phrase in memory_triggers
        ):
            memory.save_long_term_memory(
                user_id,
                user_message
            )

        # ==========================================
        # STEP 9: API RESPONSE
        # ==========================================

        return {
            "response": answer,
            "understanding": understanding,
            "memory_used": bool(recent or long_term),
            "rag_sources": [
                {
                    "source": item["source"],
                    "score": round(item["score"], 3)
                }
                for item in rag_results
            ],
            "agent_decision": decision,
            "tool_result": tool_result
        }

    except HTTPException:
        raise

    except Exception as exc:
        # Log the detailed error in the terminal.
        print(f"Error in /chat endpoint: {exc}")

        raise HTTPException(
            status_code=500,
            detail=(
                "An error occurred while processing your "
                "message. Check the VS Code terminal for details."
            )
        ) from exc
