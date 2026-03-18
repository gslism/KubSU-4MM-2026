const MAX_TEXT_LENGTH = 1_000;

function parseTextContent(maxLen) {
  if (!document.body?.innerText) {
    return "";
  }
  return document.body.innerText.trim().slice(0, maxLen);
}

function getTextBySelectors(selectors) {
  const headers = [];
  document.querySelectorAll(selectors).forEach((el) => {
    const text = (el.innerText || "").trim();
    if (text) headers.push(text);
  });
  return headers.join(". ");
}

window.addEventListener('load', (event) => {
  const payload = {
    type: "view",
    url: location.href,
    title: document.title || "",
    lang: document.documentElement?.lang || "",
    text: parseTextContent(MAX_TEXT_LENGTH),
    headers: getTextBySelectors("h1, h2, h3")
  };

  chrome.runtime.sendMessage(payload);
});