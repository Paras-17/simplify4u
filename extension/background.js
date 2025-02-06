chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
      id: "show_selected_text",
      title: "Show Selected Text",
      contexts: ["selection"]
    });
    chrome.contextMenus.create({
      id: "summarise",
      title: "Summarise Selected Text",
      contexts: ["selection"]
    });
    chrome.contextMenus.create({
      id: "translate",
      title: "Translate Selected Text",
      contexts: ["selection"]
    });
    chrome.contextMenus.create({
      id: "analyse",
      title: "Analyse Selected Text",
      contexts: ["selection"]
    });
});

// Context menu click handler
chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === "show_selected_text") {
        chrome.scripting.executeScript({
            target: { tabId: tab.id },
            function: getSelectedText, // Function to get selected text
        });
    } else if (info.menuItemId === "summarise") {
        chrome.scripting.executeScript({
            target: { tabId: tab.id },
            function: summarise, // Function to summarise selected text
        });
    } else if (info.menuItemId === "translate") {
        chrome.scripting.executeScript({
            target: { tabId: tab.id },
            function: translate, // Function to translate selected text
        });
    } else if (info.menuItemId === "analyse") {
        chrome.scripting.executeScript({
            target: { tabId: tab.id },
            function: analyse, // Function to analyse selected text
        });
    }
});

// Functions for selected text actions (now injected into the page context)
function getSelectedText() {
    const selectedText = window.getSelection().toString();
    if (selectedText) {
        alert(`You selected: ${selectedText}`);
    }
}

function summarise() {
    const selectedText = window.getSelection().toString();
    if (selectedText) {
        alert(`Summarising: ${selectedText}`);
    }
}

function translate() {
    const selectedText = window.getSelection().toString();
    if (selectedText) {
        alert(`Translating: ${selectedText}`);
    }
}

function analyse() {
    const selectedText = window.getSelection().toString();
    if (selectedText) {
        alert(`Analysing: ${selectedText}`);
    }
}
