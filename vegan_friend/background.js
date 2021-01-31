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
    chrome.storage.sync.set({roast: value.roast}, function() {
      chrome.tabs.sendMessage(tabId, {'method': value.roast});
    });
  }

  /////// FOR TESTING
  // chrome.storage.sync.set({roast: value}, function() {
  //   chrome.tabs.sendMessage(tabId, {'method': value});
  // });

}

// When the browser-action button is clicked...
chrome.webNavigation.onCompleted.addListener(function (details) {

    // ...check the URL of the active tab against our pattern and...
    if (urlRegex.test(details.url)) {
        // ...if it matches, send a message specifying a callback too
        let output = Promise.resolve(parseDom(details.url));
        output.then(value => showResponse(details.tabId, value));

        /////// FOR TESTING
        // showResponse(details.tabId, "MEATS");
      }
});
