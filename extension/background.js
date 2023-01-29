// A function to use as callback
function doStuffWithDom(domContent) {
    console.log('I received the following DOM content:\n' + domContent);
}

// When the browser-action button is clicked...
chrome.browserAction.onClicked.addListener(function (tab) {
    // ...check the URL of the active tab against our pattern and...
    chrome.tabs.sendMessage(tab.id, {text: 'report_back'}, doStuffWithDom);
});

chrome.tabs.onCreated.addListener(function(tab) {
    console.log(tab.id);
  });
  