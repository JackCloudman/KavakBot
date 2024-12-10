document.addEventListener('DOMContentLoaded', () => {
    const welcomeScreen = document.getElementById('welcomeScreen');
    const chatContainer = document.getElementById('chatContainer');
    const welcomeForm = document.getElementById('welcomeForm');
    const chatForm = document.getElementById('chatForm');
    const chatMessages = document.getElementById('chatMessages');
    const messageInput = document.getElementById('messageInput');
    const numbersInput = document.getElementById('numbers');
    const thinkingIndicator = document.getElementById('thinkingIndicator');
    
    let currentUser = '';
    let backendUrl = localStorage.getItem('backendUrl') || 'http://localhost:8080';

    // Initialize backend URL from localStorage if available
    document.getElementById('backendUrl').value = backendUrl;

    // Toggle advanced settings panel
    document.getElementById('toggleAdvanced').addEventListener('click', () => {
        const button = document.getElementById('toggleAdvanced');
        const panel = document.getElementById('advancedPanel');
        button.classList.toggle('active');
        panel.classList.toggle('active');
    });

    // Save backend URL when changed
    document.getElementById('backendUrl').addEventListener('change', (e) => {
        backendUrl = e.target.value;
        localStorage.setItem('backendUrl', backendUrl);
    });

    // Add input validation for numbers
    numbersInput.addEventListener('input', (e) => {
        e.target.value = e.target.value.replace(/\D/g, '').slice(0, 4);
    });

    welcomeForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const numbers = document.getElementById('numbers').value;

        if (numbers.length !== 4) {
            alert('Por favor ingresa exactamente 4 números');
            return;
        }

        currentUser = `${username}#${numbers}`;
        welcomeScreen.style.display = 'none';
        chatContainer.style.display = 'flex';

        // Reset logo animation
        const chatLogo = document.querySelector('.chat-logo');
        chatLogo.style.animation = 'none';
        chatLogo.offsetHeight; // Trigger reflow
        chatLogo.style.animation = 'slideDown 0.5s ease forwards';

        // Add welcome message after a slight delay to let the animation complete
        setTimeout(() => {
            addMessage(`¡Hola ${username}! Soy NeoKavakBot, un asistente virtual de la empresa Kavak. Estoy aquí para ayudarte con todas tus consultas sobre compra, venta y financiamiento de autos, así como para resolver dudas sobre nuestros servicios y políticas. 🚗💬 ¡Cuenta conmigo para tener la mejor experiencia con Kavak!`, 'bot');
        }, 500);
    });

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = messageInput.value.trim();
        
        if (message) {
            addMessage(message, 'user');
            messageInput.value = '';
            
            // Show thinking indicator
            thinkingIndicator.style.display = 'block';
            chatMessages.scrollTop = chatMessages.scrollHeight;

            try {
                const response = await fetch(`${backendUrl}/api/v1/chat/webhook/whatsappp`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'accept': 'application/json'
                    },
                    body: JSON.stringify({
                        message: message,
                        phone_number: currentUser
                    })
                });

                const data = await response.json();
                // Hide thinking indicator before showing the response
                thinkingIndicator.style.display = 'none';
                addMessage(data.response, 'bot');
            } catch (error) {
                console.error('Error:', error);
                // Hide thinking indicator in case of error
                thinkingIndicator.style.display = 'none';
                addMessage('Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta de nuevo.', 'bot');
            }
        }
    });

    function addMessage(text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${type}-message`);
        
        if (type === 'bot') {
            // Use marked to parse markdown for bot messages
            messageDiv.innerHTML = marked.parse(text);
        } else {
            // For user messages, keep using plain text
            messageDiv.textContent = text;
        }
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
