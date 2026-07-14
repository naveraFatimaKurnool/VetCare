// ========================================
// Meadow Vet Care - Chat Widget JavaScript
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const chatWidget = document.getElementById('chatWidget');
    const chatToggle = document.getElementById('chatToggle');
    const closeChatBtn = document.getElementById('closeChatBtn');
    const chatForm = document.getElementById('chatForm');
    const userInput = document.getElementById('userInput');
    const chatMessages = document.getElementById('chatMessages');
    const sendBtn = document.getElementById('sendBtn');
    const resetBtn = document.getElementById('resetBtn');

    // Initialize
    init();

    function init() {
        // Event Listeners
        chatForm.addEventListener('submit', handleFormSubmit);
        closeChatBtn.addEventListener('click', closeChat);
        resetBtn.addEventListener('click', handleReset);
        
        // Navbar scroll effect
        window.addEventListener('scroll', handleScroll);
        
        // Smooth scroll for nav links
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', handleNavClick);
        });
    }

    // ========================================
    // Chat Functions
    // ========================================

    function handleFormSubmit(e) {
        e.preventDefault();
        
        const message = userInput.value.trim();
        if (!message) return;
        
        // Add user message
        addMessage(message, 'user');
        userInput.value = '';
        
        // Show typing indicator
        showTypingIndicator();
        
        // Disable input
        setInputEnabled(false);
        
        // Send to backend
        sendMessage(message);
    }

    async function sendMessage(message) {
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });
            
            const data = await response.json();
            
            removeTypingIndicator();
            addMessage(data.response, 'bot');
            
        } catch (error) {
            removeTypingIndicator();
            addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            console.error('Error:', error);
        }
        
        setInputEnabled(true);
        userInput.focus();
    }

    function addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatar = sender === 'bot' ? '🐾' : '👤';
        const time = getCurrentTime();
        
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <span>${avatar}</span>
            </div>
            <div class="message-content">
                <div class="message-bubble">
                    ${formatMessage(content)}
                </div>
                <span class="message-time">${time}</span>
            </div>
        `;
        
        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }

    function formatMessage(content) {
        // Convert markdown-like formatting
        let formatted = content
            // Bold text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            // Italic text
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            // Line breaks
            .replace(/\n/g, '<br>')
            // Bullet points
            .replace(/•/g, '&bull;')
            // Simple lists
            .replace(/^- (.*)/gm, '<li>$1</li>')
            .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
        
        return formatted;
    }

    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-message';
        typingDiv.innerHTML = `
            <div class="message-avatar">
                <span>🐾</span>
            </div>
            <div class="message-content">
                <div class="message-bubble">
                    <div class="typing-indicator">
                        <span class="typing-dot"></span>
                        <span class="typing-dot"></span>
                        <span class="typing-dot"></span>
                    </div>
                </div>
            </div>
        `;
        chatMessages.appendChild(typingDiv);
        scrollToBottom();
    }

    function removeTypingIndicator() {
        const typing = document.querySelector('.typing-message');
        if (typing) typing.remove();
    }

    function handleReset() {
        fetch('/api/reset', { method: 'POST' })
            .then(() => {
                chatMessages.innerHTML = '';
                addWelcomeMessage();
            })
            .catch(error => console.error('Reset error:', error));
    }

    function addWelcomeMessage() {
        const welcomeHTML = `
            <div class="message bot-message">
                <div class="message-avatar">
                    <span>🐾</span>
                </div>
                <div class="message-content">
                    <div class="message-bubble">
                        <p class="greeting">Hello! 👋 I'm your VetCare Assistant.</p>
                        <p>I can help you with:</p>
                        <div class="quick-actions">
                            <button class="quick-btn" onclick="sendQuickMessage('What services do you offer?')">🔍 Services</button>
                            <button class="quick-btn" onclick="sendQuickMessage('Show me prices')">💰 Prices</button>
                            <button class="quick-btn" onclick="sendQuickMessage('Check availability')">📅 Availability</button>
                            <button class="quick-btn" onclick="sendQuickMessage('Any special offers?')">🎁 Offers</button>
                        </div>
                        <p class="help-text">Or just type your question below!</p>
                    </div>
                    <span class="message-time">Just now</span>
                </div>
            </div>
        `;
        chatMessages.innerHTML = welcomeHTML;
    }

    // ========================================
    // UI Functions
    // ========================================

    function setInputEnabled(enabled) {
        sendBtn.disabled = !enabled;
        userInput.disabled = !enabled;
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function getCurrentTime() {
        return new Date().toLocaleTimeString('en-US', { 
            hour: 'numeric', 
            minute: '2-digit',
            hour12: true 
        });
    }

    // ========================================
    // Chat Toggle Functions
    // ========================================

    window.toggleChat = function() {
        chatWidget.classList.add('active');
        chatToggle.style.display = 'none';
        userInput.focus();
    };

    function closeChat() {
        chatWidget.classList.remove('active');
        chatToggle.style.display = 'flex';
    }

    window.openChat = function() {
        chatWidget.classList.add('active');
        chatToggle.style.display = 'none';
        userInput.focus();
        
        // Smooth scroll to chat section if needed
        const chatSection = document.getElementById('home');
        if (chatSection) {
            chatSection.scrollIntoView({ behavior: 'smooth' });
        }
    };

    // ========================================
    // Quick Message Function
    // ========================================

    window.sendQuickMessage = function(message) {
        userInput.value = message;
        chatForm.dispatchEvent(new Event('submit'));
    };

    // ========================================
    // Navigation Functions
    // ========================================

    function handleScroll() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }

    function handleNavClick(e) {
        e.preventDefault();
        const targetId = e.target.getAttribute('href');
        const target = document.querySelector(targetId);
        
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
        
        // Update active state
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        e.target.classList.add('active');
    }

    // ========================================
    // Keyboard Shortcuts
    // ========================================

    document.addEventListener('keydown', function(e) {
        // Escape key to close chat
        if (e.key === 'Escape' && chatWidget.classList.contains('active')) {
            closeChat();
        }
        
        // Enter key to send (when not in input)
        if (e.key === 'Enter' && document.activeElement !== userInput && chatWidget.classList.contains('active')) {
            userInput.focus();
        }
    });
});
