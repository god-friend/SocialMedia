let HISTORY = ["home/1/"]
let current = 0;
let scrollPos = 0;

function getCookie(name){
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function changeMainSpace(response){
    document.getElementById("main-Space").innerHTML = "";
    document.getElementById("main-Space").innerHTML = response;
    $("body").removeAttr("style");
}

function postComment(event, id){

    $("#formComment-"+id).submit(function(e){
        e.preventDefault();
        
        var data = $("#formComment-"+id).serialize();

        var URL = "http://" + location.host + "/comment/";
        $.ajax(
            {
                url: URL,
                data: data,
                type: "POST",
                success: (re)=>{
                    var pid = id.split("-")[0];
                    var div = document.getElementById("collapseComment-"+pid);
                    div.innerHTML = "";
                    div.innerHTML = re;
                }
            }
        )
    } );
    
}

function deleteComment(id, pid){
    // console.log(id);
    var URL = "http://" + location.host + "/cDel/" + id;
    $.ajax({
        url: URL,
        type: "GET",
        success: (res)=>{
            var div = document.getElementById("collapseComment-"+pid);
            div.innerHTML = "";
            div.innerHTML = res;
        }
    })

}

function postFormAjax(endpoint, formData){
    var URL = "http://" + location.host + "/" + endpoint + "/";

    $.ajax({
        type: "POST",
        url: URL,
        data: formData,
        contentType: false,
        processData: false,
        success: (response) => {
            changeMainSpace(response);
        }
    })
}

function getFormAjax(endpoint, formData){
    var URL = "http://" + location.host + "/" + endpoint + "/";

    $.ajax({
        type: "GET",
        url: URL,
        data: formData,
        contentType: false,
        processData: false,
        success: (response) =>{
            changeMainSpace(response);
        }
    })
}

function getAjaxRequest(endpoint){
    var URL = "http://" + location.host + "/" + endpoint;

    $.ajax({
        type: "GET",
        url: URL,
        success: (response)=>{
            changeMainSpace(response);
        }
    })
}

function goHome(){
    getAjaxRequest("home/1/");
    HISTORY.push("home/1/");
    current += 1;
    window.scrollTo(0, scrollPos);
}

function goToAccount(){
    getAjaxRequest("account/");
}

function goToUploads(n){
    getAjaxRequest("uploads/"+n+"/");
    HISTORY.push("uploads/"+n+"/");
    current += 1;
}

function goToNextPage(query){
    getAjaxRequest(query);
}

function goToPreviousPage(query){
    getAjaxRequest(query);
}

function showFullPost(pid, scrollP){
    getAjaxRequest("post/"+pid+"/");
    history.scrollRestoration = "manual";
    window.scrollTo(0, 0);
    HISTORY.push("post/"+pid+"/");
    current += 1;
}

function searchUsers(){
    $("#searchUserForm").submit(
        function (e){
            e.preventDefault();
            var form = $("#searchUserForm").serialize();
            getFormAjax("search", form);
        }
    );    
}

function sendRequest(url){
    getAjaxRequest(url);
}

function cancelRequest(url){
    getAjaxRequest(url);
}

function getRequests(){
    getAjaxRequest("requests");
}

function acceptRequest(url){
    getAjaxRequest(url);
}

function rejectRequest(url){
    getAjaxRequest(url);
}

function getNotifications(){
    getAjaxRequest("notifications");
    HISTORY.push("notifications");
    current += 1;
}

function readNotification(url){
    getAjaxRequest(url);
    HISTORY.push(url);
    current += 1;
}

function goToFriends(){
    getAjaxRequest("friends");
    HISTORY.push("friends");
    current += 1;
}

function getFriendFeed(id){
    getAjaxRequest("fFeed/"+id+"/");
    HISTORY.push("fFeed/"+id+"/");
    current += 1;
}

function goToMyPosts(){
    getAjaxRequest("myPosts");
    HISTORY.push("myPosts");
    current += 1;
}

function goBack(){
    if(current > 0){
        HISTORY.pop();
        current -= 1;
        getAjaxRequest(HISTORY[current]);
    }
    
}


function deletePost(loc, pid){
    getAjaxRequest("deletePosts/"+pid+"/?loc="+loc);
}

function deleteProfilePic(pic){
    getAjaxRequest("delProPic/?pLoc="+pic);
}

function markAllRead(){
    getAjaxRequest("markRead");
}

function changeUserInfo(){
    $("#changeUserInfoForm").submit(function(e){
        e.preventDefault();
        var form = $("#changeUserInfoForm")[0];
        var form_Data = new FormData(form);
        // console.log(form);
        postFormAjax("account", form_Data);
    })
}

function newPost(){
    $("#newPostForm").submit(
        function (e){
            e.preventDefault();
            var form = $("#newPostForm")[0];
            var form_Data = new FormData(form)
            console.log();
            postFormAjax("home", form_Data);
        }
    )
}

