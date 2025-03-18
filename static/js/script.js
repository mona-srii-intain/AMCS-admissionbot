document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatBody = document.getElementById('chat-body');
    
    // Function to add message to chat
    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
        
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        
        // Format messages with line breaks
        const formattedMessage = message.replace(/\n/g, '<br>');
        messageContent.innerHTML = `<p>${formattedMessage}</p>`;
        
        const timestamp = document.createElement('div');
        timestamp.classList.add('message-time');
        
        // Format current time
        const now = new Date();
        const hours = now.getHours().toString().padStart(2, '0');
        const minutes = now.getMinutes().toString().padStart(2, '0');
        timestamp.textContent = `${hours}:${minutes}`;
        
        messageDiv.appendChild(messageContent);
        messageDiv.appendChild(timestamp);
        chatBody.appendChild(messageDiv);
        
        // Scroll to the bottom
        chatBody.scrollTop = chatBody.scrollHeight;
    }
    
    // Add typing indicator
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'bot-message', 'typing-indicator');
        
        const typingContent = document.createElement('div');
        typingContent.classList.add('message-content');
        typingContent.innerHTML = '<p>Typing<span class="dot">.</span><span class="dot">.</span><span class="dot">.</span></p>';
        
        typingDiv.appendChild(typingContent);
        chatBody.appendChild(typingDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
        
        return typingDiv;
    }
    
    // Remove typing indicator
    function removeTypingIndicator(indicator) {
        if (indicator && indicator.parentNode) {
            indicator.parentNode.removeChild(indicator);
        }
    }
    
    // Handle form submission
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const message = userInput.value.trim();
        
        if (message) {
            // Add user message to chat
            addMessage(message, true);
            
            // Clear input
            userInput.value = '';
            
            // Show typing indicator
            const typingIndicator = showTypingIndicator();
            
            // Send message to server
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    'message': message
                })
            })
            .then(response => response.json())
            .then(data => {
                // Remove typing indicator
                removeTypingIndicator(typingIndicator);
                
                // Add bot response to chat
                addMessage(data.response);
                
                // Log confidence for debugging
                console.log(`Response confidence: ${data.confidence}%`);
            })
            .catch(error => {
                removeTypingIndicator(typingIndicator);
                console.error('Error:', error);
                addMessage('Sorry, I encountered an error. Please try again later.');
            });
        }
    });
    
    // Focus on input field when page loads
    userInput.focus();
});