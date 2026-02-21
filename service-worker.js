    
    chrome.runtime.onMessage.addListener((request,sender,sendResponse) => {
        if (request.action === "sendData")
        {
            console.log("Получен заголовок от контент-скрипта", request.headers);
        }
    });
