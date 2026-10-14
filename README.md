# AI IT Helpdesk & Troubleshooting Agent 🤖

An AI-powered helpdesk application built using **Python, FastAPI, Google Gemini, Retrieval-Augmented Generation (RAG), conversation memory, and SQLite**. The application allows users to ask questions in natural language and receive AI-generated assistance using information from a knowledge base.

## 🚀 Project Overview

The AI IT Helpdesk & Troubleshooting Agent is designed to simplify IT support by providing conversational assistance for common user queries. It combines a Large Language Model (LLM) with knowledge retrieval, memory, and backend tools to generate relevant responses.

The application follows this workflow:

**User Query → LLM → Memory → RAG → Agent → Tools → Response**

- **LLM:** Understands user queries and generates responses using Google Gemini.
- **Memory:** Maintains relevant conversation context.
- **RAG:** Retrieves information from company FAQs, product documentation, and policies.
- **AI Agent:** Coordinates the processing flow and selects supported actions.
- **Tools:** Provides access to the application's implemented support utilities.
- **Database:** Stores relevant application and conversation data.

## ✨ Key Features

- **AI-powered chat:** Interact with the helpdesk using natural language.
- **Gemini integration:** Generate conversational responses using Google's Gemini API.
- **Knowledge-base retrieval:** Use relevant documentation to support answers through RAG.
- **Conversation memory:** Maintain context across messages.
- **FastAPI backend:** Handle chat requests through REST API endpoints.
- **SQLite database:** Support local data persistence.
- **Interactive web interface:** Chat with the assistant through an HTML, CSS, and JavaScript frontend.
- **Error handling:** Provide clearer feedback when the AI service is temporarily unavailable.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| FastAPI | Backend API development |
| Google Gemini API | LLM integration |
| RAG | Knowledge retrieval and context grounding |
| SQLite | Local database |
| HTML, CSS, JavaScript | Frontend interface |
| Uvicorn | ASGI development server |
| Sentence Transformers / FAISS | Semantic embeddings and vector retrieval, if enabled in the current implementation |

## 📂 Project Structure

```text
ai-it-helpdesk-agent/
│
├── app.py
├── agent.py
├── config.py
├── database.py
├── memory.py
├── rag.py
├── llm.py
├── tools.py
│
├── knowledge_base/
│   ├── company_faq.txt
│   ├── product_document.txt
│   └── refund_policy.txt
│
├── templates/
│   └── index.html
│
├── static/
│   ├── styles.css
│   └── scripts.js
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

**Note:** The SQLite database file `helpdesk.db` may be created automatically when the application runs. Keep the structure in this README aligned with the files actually present in your repository.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/ai-it-helpdesk-agent.git
cd ai-it-helpdesk-agent
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory using `.env.example` as a template.

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=your_configured_gemini_model
```

Obtain an API key through [Google AI Studio](https://aistudio.google.com/apikey). Set `GEMINI_MODEL` to a model available to your API key and supported by your installed SDK.

**Important:** Never upload your actual `.env` file or API key to GitHub.

### 5. Run the application

```bash
python -m uvicorn app:app --reload
```

### 6. Open the application

- **Web application:** http://127.0.0.1:8000/
- **API documentation:** http://127.0.0.1:8000/docs
- **Health check:** http://127.0.0.1:8000/health

## 🔄 How It Works

1. The user enters a question in the chat interface.
2. FastAPI receives the request through the `/chat` endpoint.
3. The application processes the query using its LLM, memory, and retrieval components.
4. Relevant knowledge-base information is supplied to the AI when available.
5. The agent coordinates the supported processing or tool actions.
6. The generated response is returned to the web interface.
7. Relevant conversation or application data is stored according to the database implementation.

## 🔐 Security Considerations

- Store API keys in environment variables.
- Exclude `.env`, virtual environments, caches, and local database files where they contain private or personal data.
- Avoid logging API keys or sensitive user information.
- Validate user input and handle external API failures safely.
- Use appropriate authentication and access controls before deploying the application for company-wide use.

## 🚧 Future Enhancements

- Automatic IT ticket creation and prioritization.
- Escalation to a human support agent.
- Integration with real IT service management systems.
- Improved document retrieval and answer evaluation.
- User authentication and role-based access.
- Automated testing, monitoring, and deployment.

## 🎯 Learning Outcomes

This project provides practical experience in Generative AI application development, LLM integration, RAG concepts, conversational memory, REST API development, database integration, and full-stack application debugging.

## 👩‍💻 Author

**Riya Jalindar Khollam**

AI/ML | Generative AI | Python | FastAPI

