from database import (
    save_message,
    get_recent_messages,
    save_memory,
    get_memories
)


class MemoryManager:

    # -----------------------------------------
    # SHORT-TERM MEMORY
    # -----------------------------------------

    def remember_message(
        self,
        user_id,
        role,
        message
    ):

        save_message(
            user_id,
            role,
            message
        )

    def get_context(self, user_id):

        return get_recent_messages(
            user_id,
            limit=10
        )

    # -----------------------------------------
    # LONG-TERM MEMORY
    # -----------------------------------------

    def save_long_term_memory(
        self,
        user_id,
        memory
    ):

        save_memory(
            user_id,
            memory
        )

    def get_long_term_memory(
        self,
        user_id
    ):

        return get_memories(
            user_id,
            limit=10
        )