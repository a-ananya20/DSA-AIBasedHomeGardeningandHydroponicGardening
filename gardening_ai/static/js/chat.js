document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    let currentNode = 'start';

    // Function to create a message element
    function createMessageElement(message, isBot = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isBot ? 'bot' : 'user');
        messageDiv.textContent = message;
        return messageDiv;
    }

    // Function to add a message to the chat
    function addMessage(message, isBot = false) {
        const messageElement = createMessageElement(message, isBot);
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to show typing indicator
    function showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.classList.add('typing-indicator');
        indicator.id = 'typing-indicator';
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('span');
            indicator.appendChild(dot);
        }
        chatMessages.appendChild(indicator);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to remove typing indicator
    function removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }

    // Function to display bot message and options
    function displayBotMessage(response, options = {}) {
        addMessage(response, true);

        if (options && Object.keys(options).length > 0) {
            const optionsDiv = document.createElement('div');
            optionsDiv.className = 'options-buttons';

            Object.entries(options).forEach(([text, key]) => {
                const button = document.createElement('button');
                button.innerText = text;
                button.className = 'option-btn';
                button.onclick = () => {
                    addMessage(text, false);
                    sendMessage(text);
                };
                optionsDiv.appendChild(button);
            });

            chatMessages.appendChild(optionsDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    // Function to send message to the server
    async function sendMessage(message) {
        showTypingIndicator();

        try {
            const response = await fetch('/chat-message/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ message: message, current_node: currentNode })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            removeTypingIndicator();
            displayBotMessage(data.response, data.options);
            currentNode = data.current_node;
        } catch (error) {
            console.error('Error:', error);
            removeTypingIndicator();
            addMessage('Sorry, I encountered an error. Please try again.', true);
        }
    }

    // Handle form submission
    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const message = userInput.value.trim();
        if (!message) return;

        addMessage(message, false);
        userInput.value = '';
        sendMessage(message);
    });

    // Add initial greeting
    setTimeout(() => {
        displayBotMessage("Hello! I'm your hydroponic gardening assistant. How can I help you today?", {});
    }, 500);
});
