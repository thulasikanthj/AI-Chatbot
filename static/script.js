async function sendMessage() {
  let input = document.getElementById("user-input");
  let message = input.value.trim();
  if (!message) return;

  addMessage("user", message);
  input.value = "";

  try {
    let response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    let data = await response.json();
    addMessage("bot", data.reply);
  } catch (error) {
    addMessage("bot", "⚠️ Error: Could not connect to server.");
    console.error(error);
  }
}

function addMessage(sender, text) {
  let chatBox = document.getElementById("chat-box");
  let messageDiv = document.createElement("div");
  messageDiv.classList.add("message", sender);
  messageDiv.innerText = text;
  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}
