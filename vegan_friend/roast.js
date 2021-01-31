let roastDiv = document.getElementById('roastText');

chrome.storage.sync.get('roast', function(data) {
    roastDiv.innerHTML = data.roast;
  });