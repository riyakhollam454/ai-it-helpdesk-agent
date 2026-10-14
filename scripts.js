const userId = "EMP001";

const chatMessages = document.getElementById("chatMessages");
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");


function addMessage(message, sender) {

    const messageDiv = document.createElement("div");

    messageDiv.className =
        sender === "user"
            ? "message user-message"
            : "message assistant-message";


    const avatar = document.createElement("div");

    avatar.className = "message-avatar";

    avatar.innerHTML =
        sender === "user" ? "👤" : "🤖";


    const content = document.createElement("div");

    content.className = "message-content";


    const name = document.createElement("div");

    name.className = "message-name";

    name.textContent =
        sender === "user"
            ? "You"
            : "HelpDesk AI";


    const bubble = document.createElement("div");

    bubble.className = "message-bubble";

    bubble.textContent = message;


    content.appendChild(name);
    content.appendChild(bubble);

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);

    chatMessages.appendChild(messageDiv);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}


function showTyping() {

    const typingDiv = document.createElement("div");

    typingDiv.id = "typingIndicator";

    typingDiv.className = "message assistant-message";


    typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>

        <div class="message-content">

            <div class="message-name">
                HelpDesk AI
            </div>

            <div class="message-bubble">

                <div class="typing">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>

            </div>

        </div>
    `;


    chatMessages.appendChild(typingDiv);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}


function removeTyping() {

    const typing = document.getElementById("typingIndicator");

    if (typing) {
        typing.remove();
    }
}


async function sendMessage() {

    const message = messageInput.value.trim();

    if (!message) {
        return;
    }


    addMessage(message, "user");

    messageInput.value = "";

    messageInput.style.height = "auto";

    sendButton.disabled = true;

    showTyping();


    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                user_id: userId,
                message: message
            })

        });


        if (!response.ok) {

            throw new Error(
                `Server error: ${response.status}`
            );

        }


        const data = await response.json();

        removeTyping();


        addMessage(
            data.response || "I couldn't generate a response.",
            "assistant"
        );


        console.log("AI Understanding:", data.understanding);

        console.log("Memory Used:", data.memory_used);

        console.log("RAG Sources:", data.rag_sources);

        console.log("Agent Decision:", data.agent_decision);

        console.log("Tool Result:", data.tool_result);


    } catch (error) {

        removeTyping();

        console.error(error);

        addMessage(
            "⚠️ Sorry, I couldn't connect to the helpdesk server. Please make sure the FastAPI server is running.",
            "assistant"
        );

    } finally {

        sendButton.disabled = false;

        messageInput.focus();

    }
}


function sendSuggestion(message) {

    messageInput.value = message;

    sendMessage();

}


function clearChat() {

    chatMessages.innerHTML = `

        <div class="message assistant-message">

            <div class="message-avatar">
                🤖
            </div>

            <div class="message-content">

                <div class="message-name">
                    HelpDesk AI
                </div>

                <div class="message-bubble">

                    New conversation started. 👋
                    <br><br>
                    How can I help you with your IT problem?

                </div>

            </div>

        </div>

    `;

}


function handleKeyPress(event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendMessage();

    }

}


/* Auto-expand textarea */

messageInput.addEventListener("input", function () {

    this.style.height = "auto";

    this.style.height =
        Math.min(this.scrollHeight, 120) + "px";

});