// Regex-pattern to check URLs against. 
// It matches URLs like: http[s]://[...]stackoverflow.com[...]
var urlRegex = /^https?:\/\/(?:[^./?#]+\.)?stackoverflow\.com/;

// A function to use as callback
function parseDom(domContent) {
    alert('I received the following DOM content:\n' + domContent);
}

// When the browser-action button is clicked...
chrome.webNavigation.onCompleted.addListener(function (details) {
    // ...check the URL of the active tab against our pattern and...

    if (urlRegex.test(details.url)) {
        // ...if it matches, send a message specifying a callback too
        chrome.tabs.sendMessage(details.tabId, {text: 'report_back'}, parseDom);
    }
});