// Regex-pattern to check URLs against.
// It matches URLs like: http[s]://[...]stackoverflow.com[...]
var urlRegex = /^https?:\/\/(?:[^./?#]+\.)?foodnetwork\.com/;

// A function to use as callback
async function parseDom(currentUrl) {
    let parsedResponse = fetch('http://localhost:5000/meats/'+currentUrl, {method: 'GET'})
              .then(response => response.json());
    return parsedResponse;
}

function showResponse(tabId, value){
  if(value.contains_meat==true){
    chrome.tabs.sendMessage(tabId, {'method': value.roast});
  }
}

// When the browser-action button is clicked...
chrome.webNavigation.onCompleted.addListener(function (details) {
    // ...check the URL of the active tab against our pattern and...
    if (urlRegex.test(details.url)) {
        // ...if it matches, send a message specifying a callback too
        let output = Promise.resolve(parseDom(details.url));
        output.then(value => showResponse(details.tabId, value));

      }
});
