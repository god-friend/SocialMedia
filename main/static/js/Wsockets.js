ws = new WebSocket("ws://"+location.host+"/sync/");

ws.onopen = function(e){
    console.log("connected");
    // ws.send("hello there");
}

ws.onmessage = function(e){
    var alertDiv = document.getElementById("liveAlertPlaceholder");
    var requestCountDiv = document.getElementById("requests-count");
    var notifyCountDiv = document.getElementById("notify-count");

    var data = JSON.parse(e['data']);
    if(data["html"] != undefined){
        alertDiv.innerHTML += data["html"];
    }
    if(data["count"] != undefined){
        requestCountDiv.innerText = "";
        requestCountDiv.innerText = data["count"];
    }
    if(data["ncount"] != undefined){
        notifyCountDiv.innerText = "";
        notifyCountDiv.innerText = data["ncount"];
    }
    
    setTimeout(function(e){
        alertDiv.innerHTML = "";
    }, 5000);
}