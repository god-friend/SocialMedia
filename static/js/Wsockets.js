ws = new WebSocket("ws://"+location.host+"/sync/");

ws.onopen = function(e){
    console.log("connected");
}

ws.onmessage = function(e){
    var requestCountDiv = document.getElementById("requests-count");
    var notifyCountDiv = document.getElementById("notify-count");
    var notificationBody = document.getElementById("notificationBody");
    

    var data = JSON.parse(e['data']);
    console.log(data);
    if(data["gotComment"] != undefined){    
        notificationBody.innerText = "";
        notificationBody.innerText = data["gotComment"];
    }else if(data["gotRequest"] != undefined){
        notificationBody.innerText = "";
        notificationBody.innerText = data["gotRequest"];
    }else if(data["gotNewPost"] != undefined){
        notificationBody.innerText = "";
        notificationBody.innerText = data["gotNewPost"];
    }
    
    if(data["count"] != undefined){
        requestCountDiv.innerText = "";
        requestCountDiv.innerText = data["count"];
    }
    if(data["ncount"] != undefined){
        notifyCountDiv.innerText = "";
        notifyCountDiv.innerText = data["ncount"];
    }

    $("#toastNotify").toast("show");
    
}