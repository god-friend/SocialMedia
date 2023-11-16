
window.onpopstate = (e) => {
    location.reload();
}

function changeHistoryState(endpoint){
    history.pushState(null, null, "/"+endpoint);
}

function closeNavOnClick(){
    var width = (window.innerWidth > 0) ? window.innerWidth : screen.width;
    if (width < 1000){
        document.getElementById("mainSideBar").style.width = "0";
        var openNavBtn = document.getElementById("openNavBtn");
        openNavBtn.style.display = "table-cell";
    }
}

function getCookie(name){
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function changeMainSpace(divId, response){
    if(divId == "main-Space"){
        var toastPlace = document.getElementById("toastPlacement");
        document.getElementById(divId).innerHTML = "";
        document.getElementById(divId).appendChild(toastPlace);
        document.getElementById(divId).innerHTML += response;
    }else{
        document.getElementById(divId).innerHTML = "";
        document.getElementById(divId).innerHTML = response;
    }
    
    $("body").removeAttr("style");
}

function likePost(divId, url){
    getAjaxRequest(divId, url);
}

function unlikePost(divId, url){
    getAjaxRequest(divId, url);
}

function postComment(event, id){

    $("#formComment-"+id).submit(function(e){
        e.preventDefault();
        
        var data = $("#formComment-"+id).serialize();

        var URL = "http://" + location.host + "/api/postComment/";
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

    var URL = "http://" + location.host + "/api/delComment/" + id;
    $.ajax({
        url: URL,
        type: "DELETE",
        headers: {
            "X-Csrftoken": getCookie("csrftoken"),
        },
        success: (res)=>{
            var div = document.getElementById("collapseComment-"+pid);
            div.innerHTML = "";
            div.innerHTML = res;
        }
    })

}

function postFormAjax(divId,endpoint, formData){
    var URL = "http://" + location.host + "/" + endpoint + "/";

    $.ajax({
        type: "POST",
        url: URL,
        data: formData,
        contentType: false,
        processData: false,
        success: (response) => {
            changeMainSpace(divId,response);
        }
    })
}

function getFormAjax(divId, endpoint, formData){
    var URL = "http://" + location.host + "/" + endpoint + "/";

    $.ajax({
        type: "GET",
        url: URL,
        data: formData,
        contentType: false,
        processData: false,
        success: (response) =>{
            changeMainSpace(divId, response);
        }
    })
}

function getAjaxRequest(divId, endpoint){
    var URL = "http://" + location.host + "/" + endpoint;

    $.ajax({
        type: "GET",
        url: URL,
        success: (response)=>{
            changeMainSpace(divId, response);
        }
    })
}

function newPost(){
    $("#newPostForm").submit(
        function (e){
            e.preventDefault();
            var form = $("#newPostForm")[0];
            var form_Data = new FormData(form)

            postFormAjax("main-Space","api/feedPage", form_Data);
        }
    )
}

function goHome(){
    getAjaxRequest("main-Space","api/feedPage");
    changeHistoryState("home/");
    window.scrollTo(0,0);
    closeNavOnClick();
}

function showFullPost(divId, url){
    getAjaxRequest(divId, url);
    window.scrollTo(0,0);
}

function goToAccount(){
    getAjaxRequest("main-Space","api/account/");
    changeHistoryState("account/");
    window.scrollTo(0,0);
    closeNavOnClick();
}

function changeUserInfo(){
    $("#changeUserInfoForm").submit(function(e){
        e.preventDefault();
        var form = $("#changeUserInfoForm")[0];
        var form_Data = new FormData(form);

        postFormAjax("nav-Space", "api/myAccount", form_Data);
    })
}

function showUserInfo(){
    getAjaxRequest("nav-Space", "api/myAccount");
}

function showUploads(){
    getAjaxRequest("nav-Space", "api/uploads");
    window.scrollTo(0,0);
}

function showProfilePics(){
    getAjaxRequest("nav-Space", "api/proPics");
    window.scrollTo(0,0);
}

function showPostPics(){
    getAjaxRequest("nav-Space", "api/postPics");
    window.scrollTo(0,0);
}

function deletePic(picPath){
    getAjaxRequest("nav-Space","api/deletePics/"+picPath);
}

function showFriends(){
    getAjaxRequest("nav-Space", "api/myFriends");
    window.scrollTo(0,0);
}

function showMyPosts(){
    getAjaxRequest("nav-Space", "api/myPosts");
    window.scrollTo(0,0);
}

function deletePost(divId, url){
    getAjaxRequest(divId, url);
}

function goToNextPage(divId, query){
    getAjaxRequest(divId, query);
    window.scrollTo(0,0);
}

function goToPreviousPage(divId, query){
    getAjaxRequest(divId, query);
    window.scrollTo(0,0);
}

function goToSearch(){
    getAjaxRequest("main-Space", "api/searchPage");
    changeHistoryState("search/");
    window.scrollTo(0,0);
    closeNavOnClick();
}

function searchUsers(){
    $("#searchUserForm").submit(
        function (e){
            e.preventDefault();
            var form = $("#searchUserForm").serialize();
            getFormAjax("searchResult","api/searchUsers", form);
        }
    );    
}

function sendRequest(url){
    getAjaxRequest("searchResult", url);
}

function cancelRequest(divId, url){
    getAjaxRequest(divId, url);
}

function getRequests(){
    getAjaxRequest("main-Space", "api/requestPage");
    changeHistoryState("requests/");
    window.scrollTo(0,0);
    closeNavOnClick();
}

function acceptRequest(divId, url){
    getAjaxRequest(divId, url);
}

function rejectRequest(divId, url){
    getAjaxRequest(divId, url);
}

function unfriend(divId, url){
    getAjaxRequest(divId, url);
}

function getFriendFeed(id){
    getAjaxRequest("nav-Space", "api/friendFeed/" + id);
    window.scrollTo(0,0);
}

function getNotifications(){
    getAjaxRequest("main-Space", "api/getNots");
    changeHistoryState("notifications/");
    window.scrollTo(0,0);
    closeNavOnClick();
}

function getNotificationPage(page){
    getAjaxRequest("main-Space", "api/getNots/?page="+page);
    window.scrollTo(0,0);
}

function readNotification(url){
    getAjaxRequest("main-Space", url);
    window.scrollTo(0,0);
}

function markAllRead(){
    getAjaxRequest("main-Space", "api/readAllNots");
}





