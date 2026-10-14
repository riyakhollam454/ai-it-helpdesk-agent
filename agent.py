import json

from llm import GeminiLLM

from tools import execute_tool


class HelpdeskAgent:

    # Only these actions are allowed
    ALLOWED_ACTIONS = {

        "none",

        "lookup_order",

        "check_refund_status",

        "create_ticket",

        "get_ticket_status",

        "send_email"
    }

    def __init__(
        self,
        llm: GeminiLLM
    ):

        self.llm = llm

    # ==================================================
    # AGENT DECISION
    # ==================================================

    def decide(
        self,
        user_message,
        understanding,
        memory_context,
        rag_context
    ):

        prompt = f"""
You are the action-planning Agent
for an AI IT Helpdesk.

Decide whether a tool is required.

Allowed actions ONLY:

none
lookup_order
check_refund_status
create_ticket
get_ticket_status
send_email

Return ONLY valid JSON.

Format:

{{
    "action": "action_name",
    "reason": "short explanation",
    "parameters": {{}}
}}

Rules:

- Do not invent IDs.
- Use lookup_order for order questions.
- Use check_refund_status for refund questions.
- Use get_ticket_status for ticket status.
- Use create_ticket when human support is required.
- Use send_email only when the user explicitly asks.
- Otherwise choose none.

USER MESSAGE:

{user_message}


LLM UNDERSTANDING:

{json.dumps(
    understanding,
    indent=2
)}


MEMORY:

{memory_context}


RAG KNOWLEDGE:

{rag_context}
"""

        raw = self.llm.generate(
            prompt
        )

        try:

            decision = json.loads(
                raw
            )

        except json.JSONDecodeError:

            decision = {
                "action": "none",
                "reason": (
                    "Could not safely "
                    "parse an action."
                ),
                "parameters": {}
            }

        # Security validation
        if (
            decision.get("action")
            not in self.ALLOWED_ACTIONS
        ):

            decision["action"] = "none"

            decision["parameters"] = {}

        return decision

    # ==================================================
    # EXECUTE AGENT ACTION
    # ==================================================

    def run(
        self,
        user_id,
        user_message,
        understanding,
        memory_context,
        rag_context
    ):

        decision = self.decide(
            user_message,
            understanding,
            memory_context,
            rag_context
        )

        # No tool required
        if decision["action"] == "none":

            return decision, None

        # Execute selected tool
        result = execute_tool(
            user_id,
            decision["action"],
            decision.get(
                "parameters",
                {}
            )
        )

        return decision, result