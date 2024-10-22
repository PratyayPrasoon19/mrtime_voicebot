// Initialize variables
const startBtn = document.getElementById('start-btn');
const conversationDiv = document.getElementById('conversation');

// Speech recognition (STT)
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'en-US';
recognition.interimResults = false;

// Speech synthesis (TTS)
function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    window.speechSynthesis.speak(utterance);
}

// Start voice recognition
startBtn.addEventListener('click', () => {
    recognition.start();
});

// When speech is recognized
recognition.onresult = (event) => {
    const userInput = event.results[0][0].transcript;
    addMessage('User: ' + userInput);

    // Send recognized text to Flask backend
    fetch('/get-response', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: userInput })
    })
    .then(response => response.json())
    .then(data => {
        const botResponse = data.reply;
        addMessage('Bot: ' + botResponse);
        speak(botResponse); // Speak out the response
    });
};

// Add a message to the chat
function addMessage(message) {
    const msg = document.createElement('p');
    msg.textContent = message;
    conversationDiv.appendChild(msg);
}

// Handle recognition errors
recognition.onerror = (event) => {
    console.log('Speech recognition error', event.error);
};
