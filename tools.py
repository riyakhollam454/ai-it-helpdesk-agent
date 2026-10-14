from datetime import datetime
from uuid import uuid4

from database import get_connection


# ==================================================
# MOCK ORDER DATABASE
# ==================================================

ORDERS = {

    "ORD1001": {
        "order_id": "ORD1001",
        "user_id": "EMP001",
        "product": "Wireless Keyboard",
        "status": "Delivered",
        "amount": 1499,
        "delivery_date": "2026-10-03"
    },

    "ORD1002": {
        "order_id": "ORD1002",
        "user_id": "EMP001",
        "product": "USB-C Hub",
        "status": "Shipped",
        "amount": 2299,
        "delivery_date": "Expected 2026-10-10"
    },

    "ORD1003": {
        "order_id": "ORD1003",
        "user_id": "EMP002",
        "product": "Laptop Stand",
        "status": "Processing",
        "amount": 999,
        "delivery_date": "Expected 2026-10-12"
    }
}


# ==================================================
# ORDER LOOKUP
# ==================================================

def lookup_order(
    user_id,
    order_id
):

    order = ORDERS.get(
        order_id
    )

    if not order:

        return {
            "success": False,
            "message": (
                f"Order {order_id} "
                "was not found."
            )
        }

    # Authorization check
    if order["user_id"] != user_id:

        return {
            "success": False,
            "message": (
                "You are not authorized "
                "to access this order."
            )
        }

    return {
        "success": True,
        "order": order
    }


# ==================================================
# REFUND STATUS
# ==================================================

def check_refund_status(
    user_id,
    order_id
):

    result = lookup_order(
        user_id,
        order_id
    )

    if not result["success"]:
        return result

    order = result["order"]

    if order["status"] == "Delivered":

        return {
            "success": True,
            "refund_status": (
                "Eligible for review"
            ),
            "message": (
                "The order is delivered "
                "and can be submitted "
                "for refund review."
            )
        }

    return {
        "success": True,
        "refund_status": (
            "Not eligible yet"
        ),
        "message": (
            "Refund review is available "
            "after the order reaches "
            "the required status."
        )
    }


# ==================================================
# CREATE TICKET
# ==================================================

def create_ticket(
    user_id,
    title,
    description,
    category="General",
    priority="Medium"
):

    ticket_id = (
        f"INC-{uuid4().hex[:8].upper()}"
    )

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO tickets
        (
            ticket_id,
            user_id,
            title,
            description,
            category,
            priority,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            ticket_id,
            user_id,
            title,
            description,
            category,
            priority,
            "Open",
            datetime.utcnow().isoformat()
        )
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "ticket_id": ticket_id,
        "status": "Open",
        "message": (
            "Support ticket created "
            "successfully."
        )
    }


# ==================================================
# GET TICKET STATUS
# ==================================================

def get_ticket_status(
    user_id,
    ticket_id
):

    conn = get_connection()

    row = conn.execute(
        """
        SELECT *
        FROM tickets
        WHERE ticket_id = ?
        AND user_id = ?
        """,
        (
            ticket_id,
            user_id
        )
    ).fetchone()

    conn.close()

    if not row:

        return {
            "success": False,
            "message": (
                "Ticket not found or "
                "you are not authorized "
                "to access it."
            )
        }

    return {
        "success": True,
        "ticket": dict(row)
    }


# ==================================================
# SEND EMAIL
# ==================================================

def send_email(
    user_id,
    recipient,
    subject,
    body
):

    # Demo implementation.
    # We store email information
    # instead of sending a real email.

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO email_log
        (
            user_id,
            recipient,
            subject,
            body,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user_id,
            recipient,
            subject,
            body,
            datetime.utcnow().isoformat()
        )
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": (
            f"Email request logged "
            f"for {recipient}."
        ),
        "recipient": recipient,
        "subject": subject
    }


# ==================================================
# TOOL ROUTER
# ==================================================

def execute_tool(
    user_id,
    action,
    parameters
):

    if action == "lookup_order":

        return lookup_order(
            user_id,
            parameters.get(
                "order_id",
                ""
            )
        )

    if action == "check_refund_status":

        return check_refund_status(
            user_id,
            parameters.get(
                "order_id",
                ""
            )
        )

    if action == "create_ticket":

        return create_ticket(
            user_id=user_id,
            title=parameters.get(
                "title",
                "IT Support Request"
            ),
            description=parameters.get(
                "description",
                ""
            ),
            category=parameters.get(
                "category",
                "General"
            ),
            priority=parameters.get(
                "priority",
                "Medium"
            )
        )

    if action == "get_ticket_status":

        return get_ticket_status(
            user_id,
            parameters.get(
                "ticket_id",
                ""
            )
        )

    if action == "send_email":

        return send_email(
            user_id=user_id,
            recipient=parameters.get(
                "recipient",
                ""
            ),
            subject=parameters.get(
                "subject",
                ""
            ),
            body=parameters.get(
                "body",
                ""
            )
        )

    return {
        "success": False,
        "message": (
            f"Unknown or unauthorized "
            f"action: {action}"
        )
    }