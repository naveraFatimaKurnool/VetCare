// ========================================
// VetCare Chatbot - JavaScript
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chatForm');
    const userInput = document.getElementById('userInput');
    const chatMessages = document.getElementById('chatMessages');
    const sendBtn = document.getElementById('sendBtn');

    // Event Listeners
    chatForm.addEventListener('submit', handleSubmit);
    userInput.addEventListener('keydown', handleKeyDown);

    function handleSubmit(e) {
        e.preventDefault();
        const message = userInput.value.trim();
        if (!message) return;

        addUserMessage(message);
        userInput.value = '';
        showTyping();
        sendMessage(message);
    }

    function handleKeyDown(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    }

    // ========================================
    // Message Functions
    // ========================================

    function addUserMessage(text) {
        const time = getTime();
        const html = `
            <div class="message user">
                <div class="avatar">👤</div>
                <div class="content">
                    <div class="bubble">
                        <p>${escapeHtml(text)}</p>
                    </div>
                    <span class="time">${time}</span>
                </div>
            </div>
        `;
        chatMessages.insertAdjacentHTML('beforeend', html);
        scrollToBottom();
    }

    function addBotMessage(text) {
        removeTyping();
        const time = getTime();
        const formatted = formatText(text);
        const html = `
            <div class="message bot">
                <div class="avatar">🐾</div>
                <div class="content">
                    <div class="bubble">
                        ${formatted}
                    </div>
                    <span class="time">${time}</span>
                </div>
            </div>
        `;
        chatMessages.insertAdjacentHTML('beforeend', html);
        scrollToBottom();
    }

    function formatText(text) {
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>')
            .replace(/•/g, '&bull;');
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // ========================================
    // Typing Indicator
    // ========================================

    function showTyping() {
        const html = `
            <div class="message bot typing-message">
                <div class="avatar">🐾</div>
                <div class="content">
                    <div class="bubble">
                        <div class="typing">
                            <span class="typing-dot"></span>
                            <span class="typing-dot"></span>
                            <span class="typing-dot"></span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        chatMessages.insertAdjacentHTML('beforeend', html);
        scrollToBottom();
    }

    function removeTyping() {
        const typing = document.querySelector('.typing-message');
        if (typing) typing.remove();
    }

    // ========================================
    // API Communication
    // ========================================

    async function sendMessage(message) {
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });

            if (!response.ok) throw new Error('Network error');

            const data = await response.json();
            addBotMessage(data.response);
        } catch (error) {
            removeTyping();
            addBotMessage('Sorry, something went wrong. Please try again.');
            console.error('Error:', error);
        }
    }

    // ========================================
    // Global Functions
    // ========================================

    window.askQuestion = function(question) {
        addUserMessage(question);
        showTyping();
        sendMessage(question);
    };

    window.newChat = function() {
        fetch('/api/reset', { method: 'POST' });
        location.reload();
    };

    window.clearChat = function() {
        if (confirm('Clear all messages?')) {
            newChat();
        }
    };

    window.showServices = function() {
        askQuestion('What services do you offer?');
    };

    window.showOffers = function() {
        askQuestion('Any special offers today?');
    };

    window.callEmergency = function() {
        window.location.href = 'tel:+15551234567';
    };

    // ========================================
    // Utilities
    // ========================================

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function getTime() {
        return new Date().toLocaleTimeString('en-US', {
            hour: 'numeric',
            minute: '2-digit',
            hour12: true
        });
    }
});
