// console.log("hello");
// // alert('hello');
// const pageTitle = document.title;
// console.log("Заголовок страницы:",pageTitle);
window.addEventListener('load',() =>
{
    const data = {
        action: "sendData",
        title: window.document.title,
        headers: getAllHeaders(window)
    };
    chrome.runtime.sendMessage(data);
}
)

function getAllHeaders(window)
{
    const result = window.document.querySelectorAll('h1');
    return Array.from(result).map(h => ({
        text: h.innerText.trim()
    }));
    return result
}
