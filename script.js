async function sendMessage() {
    const inputField = document.getElementById("input");
    const chatBox = document.getElementById("chat");
    const message = inputField.value.trim();

    if (!message) return;

    
    chatBox.innerHTML += `<div class="user-msg"><b>Vi:</b> ${message}</div>`;
    inputField.value = "";

    
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
       
        const response = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        if (data.reply) {
            
            const botDiv = document.createElement("div");
            botDiv.className = "bot-msg";
            chatBox.appendChild(botDiv);

            
            typeWriterEffect(data.reply, botDiv);
        }

    } catch (error) {
        console.error("Greška:", error);
        chatBox.innerHTML += `<div style="color:red">Sistem: Greška u vezi sa serverom.</div>`;
    }
}


function typeWriterEffect(text, element) {
    let i = 0;
    element.innerHTML = "<b>Bibliotekar:</b> ";
    
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, 15); 
            
            const chatBox = document.getElementById("chat");
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }
    type();
}