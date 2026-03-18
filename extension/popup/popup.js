const API_URL = "http://127.0.0.1:8000";

const queryInput = document.getElementById("queryInput");
const sendButton = document.getElementById("sendButton");
const historyButton = document.getElementById("historyButton");
const responseDiv = document.getElementById("response");

sendButton.addEventListener("click", () => sendRequest());
queryInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendRequest();
});

async function sendRequest() {
  const text = queryInput.value.trim();
  if (!text) return;

  sendButton.disabled = true;
  responseDiv.style.display = "block";
  responseDiv.textContent = "Загрузка...";

  try {
    const res = await fetch(`${API_URL}/request`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({"prompt": text}),
    });

    const raw = await res.text();
    if (!res.ok) throw new Error(`Ошибка: ${res.status} ${res.statusText}\n${raw}`);
    responseDiv.textContent = raw;
  } catch (err) {
    responseDiv.textContent = `Ошибка: ${err.message}`;
  } finally {
    sendButton.disabled = false;
  }
}

historyButton.addEventListener("click", () => loadHistory());

async function loadHistory() {
  historyButton.disabled = true;
  responseDiv.style.display = "block";
  responseDiv.textContent = "Загрузка...";

  try {
    const res = await fetch(`${API_URL}/history`, {
      method: "GET"
    });

    const raw = await res.text();
    if (!res.ok) throw new Error(`Ошибка: ${res.status} ${res.statusText}\n${raw}`);
    responseDiv.textContent = raw;
  } catch (err) {
    responseDiv.textContent = `Ошибка: ${err.message}`;
  } finally {
    historyButton.disabled = false;
  }
}