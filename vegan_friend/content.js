chrome.runtime.onMessage.addListener(function(message,sender,sendResponse){
    // if(message.method == 'meat'){
        alert(message.method);
        flashBackground("red", "white");
        document.title = "MEAT?!"
        document.body.innerHTML +='<div style="position:absolute;width:100%;height:100%;z-index:100;background:#000;"></div>';
        return true;
    //}
});

function flashBackground(color1, color2){
    document.body.style.backgroundColor=color1
    setTimeout(function(){ document.body.style.backgroundColor=color2;
        setTimeout(function(){ document.body.style.backgroundColor=color1;
            setTimeout(function(){ document.body.style.backgroundColor=color2;
                setTimeout(function(){ document.body.style.backgroundColor=color1;
                    setTimeout(function(){ document.body.style.backgroundColor=color2;
                    }, 500);
                }, 500);
            }, 500);
        }, 500);
    }, 500);
}