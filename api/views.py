from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator

from main.forms import ChangeUserForm
from main.models import Users, Posts
from main.models import Comments, Requests, Likes
from main.models import Friends, Notifications
from main.extras import upload_post_pics, getAllPics, delPic

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import api_view, renderer_classes


@api_view(['get'])
@renderer_classes([TemplateHTMLRenderer])
def accountPage(request, format=None):
    return Response(template_name="components/forAccount/account_page.html")


@api_view(['get'])
@renderer_classes([TemplateHTMLRenderer])
def uploadPage(request, format=None):
    latestPost = Posts.objects.filter(by=request.user).exclude(urls__urls__iexact="[]").last()
    if not latestPost:
        lUrl = None
    else:
        lUrl = latestPost.urls["urls"][0]

    pPic = request.user.profile_pic    
    if pPic:
        pPic = request.user.profile_pic.url
        
    data = {
        "profile": pPic,
        "postPics": lUrl
    }
    return Response(data, template_name="components/forUploads/uploads.html")


@api_view(['get'])
@renderer_classes([TemplateHTMLRenderer])
def showProfilePics(request, format=None):
     # Show All Profile Pics Uploaded Till Date
    userProPics = request.user.profile_pic.url
    indx = userProPics.rfind("/")
    indxs = userProPics.find("/", userProPics.find("/")+1)
    url = userProPics[:indx+1]
    allProfilePics = getAllPics(userProPics[indxs:indx])
    allProfilePicsUrl = [(url+pName) for pName in allProfilePics]
    pages = Paginator(allProfilePicsUrl, 9)
    page = request.GET.get("page")
    if(page == None):
        page = 1 

    data = {
        "show": 0,
        "pPics": pages.page(page),
        "total_pages": pages.page_range,
    }
    return Response(data, template_name="components/forUploads/showPrPics.html")   
        
        
@api_view(['get'])
@renderer_classes([TemplateHTMLRenderer])
def showPostPics(request, format=None):
     # Show All pics Uploaded By user at Feed
    posts = Posts.objects.filter(by=request.user)
    urls = []
    for x in posts:
        urls += x.urls["urls"]

    pages = Paginator(urls, 3)
    page = request.GET.get("page")
    if(page == None):
        page = 1

    data = {
        "show": 1,
        "pPics": pages.page(page),
        "total_pages": pages.page_range
    }
    return Response(data, template_name="components/forUploads/showPrPics.html")   


@api_view(['get'])
def deletePics(request):
    postPicPath = request.query_params.get("pPath")
    dpPath = request.query_params.get("dpPath")

    if postPicPath:
        picPath = postPicPath
    elif dpPath:
        picPath = dpPath
    
    # File Name
    fileNameStart = picPath.rfind("/")
    fileName = picPath[fileNameStart+1:]
    
    # File Location
    locNameStart = picPath.find("media/")
    location = picPath[locNameStart+6:fileNameStart+1]
    
    if postPicPath:
        postIdStartsFrom = location.rfind("_")
        postId = int(location[postIdStartsFrom+1:len(location)-1])
        post = Posts.objects.get(id=postId)
        urls = post.urls["urls"]
        newUrls = []
        for i in range(len(urls)):
            if urls[i] != picPath:
                newUrls.append(urls[i])
        
        post.urls["urls"] = newUrls
        post.save()
        delPic(location+fileName)
        
        return redirect("/api/postPics/")
    elif dpPath:
        delPic(location+fileName)
        
        user = Users.objects.get(id=request.user.id)
        available_profile_pics = getAllPics("/"+location)
        
        if len(available_profile_pics) > 0:
            user.profile_pic = location + available_profile_pics[0]
        else:
            user.profile_pic = "/defaults/default-user.png"
            
        user.save()
        return redirect("/api/proPics/")
    

@api_view(['get'])
@renderer_classes([TemplateHTMLRenderer])
def showfullpost(request, format=None):
    pid = request.query_params.get("pid")
    back = request.query_params.get("back")
    divId = request.query_params.get("divId")

    post = Posts.objects.get(id=pid)

    data = {
        "posts": post,
    }
    
    if back == "home":
        back = "goHome()"
        data["homeBackPage"] = "home"
    elif back == "fFeed":
        back = "getFriendFeed('{0}')".format(post.by.id)
        data["friendBackPage"] = "fFeed"
    elif back == "mePosts":
        back = "showMyPosts()"
        data["meBackPage"] = "mePosts"
    elif back == "notifications":
        page = request.query_params.get("page")
        back = "getNotificationPage('{0}')".format(page)
        data["notiBackPage"] = page
        
    data["back"] = back
    data["divId"] = divId
    
    return Response(data, template_name="components/forPosts/full_post.html")


@api_view(['get'])
@renderer_classes([TemplateHTMLRenderer])
def likePost(request, requestType):
    postId = request.query_params.get("postId")
    pageType = request.query_params.get("pageType")
    post = Posts.objects.get(id=postId)
    currentLikes = post.likes
    if requestType == 0:
        post.likes = currentLikes + 1
        post.save()
        Likes.objects.create(byUser=request.user, likedPost=post)
    elif requestType == 1:
        post.likes = currentLikes - 1
        post.save()
        lObj = Likes.objects.get(byUser=request.user, likedPost=post)
        lObj.delete()
        
    data = {
            "posts": post,
        }
    if pageType == "feedPage":
        data["loc"] = "home"
        data["goBack"] = "home"
        data["divId"] = "main-Space"
    elif pageType == "myPostsPage":
        data["loc"] = "myPosts"
        data["goBack"] = "mePosts"
        data["divId"] = "nav-Space"
    elif pageType == "friendFeedPage":
        data["loc"] = "friendFeedPage"
        data["goBack"] = "fFeed"
        data["divId"] = "nav-Space"
    elif pageType == "fullPage":
        back = request.query_params.get("back")
        divId = request.query_params.get("divId")
        url = "/api/fullPost/?pid={0}&back={1}&divId={2}".format(postId, back, divId)
        if back == "notifications":
            page = request.query_params.get("page")
            url += "&page={0}".format(page)
             
        return redirect(url)
    
    return Response(data, template_name="components/forPosts/post.html")


@api_view(['get'])
@renderer_classes([TemplateHTMLRenderer])
def searchPage(request, format=None):
    return Response(template_name="components/forSearch/searchPage.html")


@api_view(['get'])
@renderer_classes([TemplateHTMLRenderer])
def searchUsers(request, format=None):
    find = request.query_params.get("find")
    current_user = request.user
    
    query = (Q(firstname__contains=find) | Q(lastname__contains=find)) & ~Q(username=current_user)
    
    
    users = Users.objects.filter(query)
    
    pages = Paginator(users, 1)
    page = request.query_params.get("page")
    if not page:
        page = 1
    elif int(page) > pages.num_pages:
        page = pages.num_pages

    data = {
        "results": pages.page(page),
        "query": find
    }
    return Response(data, template_name="components/forSearch/searchResults.html")


@api_view(['get'])
def sendRequest(request, toUser):
    
    page = request.query_params.get("page")
    find = request.query_params.get("find")
    
    user = Users.objects.get(id=toUser)
    req = Requests(by=request.user, to=user)
    req.save()
    
    return redirect('/api/searchUsers/?find={0}&page={1}'.format(find, page))


@api_view(['get'])
def delRequest(request, byUser, toUser):
    
    page = request.query_params.get("page")
    find = request.query_params.get("find")
    
    bUser = Users.objects.get(id=byUser)
    tUser = Users.objects.get(id=toUser)
    
    req = Requests.objects.get(by=bUser, to=tUser)
    req.delete()
    
    if not page and not find:
        return redirect('/api/requestPage/')
        
    return redirect('/api/searchUsers/?find={0}&page={1}'.format(find, page))


@api_view(['get'])
@renderer_classes([TemplateHTMLRenderer])
def requestPage(request, format=None):
    got_requests = Requests.objects.filter(to=request.user)
    sended_request = Requests.objects.filter(by=request.user)

    data = {
        "got_requests": got_requests,
        "sended_requests": sended_request
    }
    return Response(data, template_name="components/forRequest/requests.html")


@api_view(['get'])
def acceptRequest(request, by):
    page = request.query_params.get("page")
    find = request.query_params.get("find")
    
    rObj = Requests.objects.get(by=by, to=request.user)
    rObj.delete()
    requestSendedBy = Users.objects.get(id=by)

    makeFriend = Friends.objects.create(user=requestSendedBy, friend=request.user)
    if not find and not page:
        return redirect("/api/requestPage/")
    
    return redirect("/api/searchUsers/?find={0}&page={1}".format(find, page))
    
    
@api_view(['get'])
def unfriendUsers(request):
    
    page = request.query_params.get("page")
    find = request.query_params.get("find")
    userId = request.query_params.get("userId")
    friendId = request.query_params.get("friendId")
    
    myUser = Users.objects.get(id=userId)
    userFriend = Users.objects.get(id=friendId)
    
    query = (Q(user=myUser) & Q(friend=userFriend)) | (Q(user=userFriend) & Q(friend=myUser))
    fObj = Friends.objects.get(query)
    fObj.delete()
    
    if not page and not find:
        return redirect("/api/myFriends")
    
    return redirect("/api/searchUsers/?find={0}&page={1}".format(find, page))


@api_view(['get'])
@renderer_classes([TemplateHTMLRenderer])
def showFriends(request, format=None):
    
    friends_id = request.user.friends()

    query = Q(id__in=friends_id)
    friends = Users.objects.filter(query)
    pages = Paginator(friends, 1)
    page = request.query_params.get("page")
    if not page:
        page = 1

    data = {
        "friends": pages.page(page)
    }

    return Response(data, template_name="components/forFriend/friends.html")


@api_view(['get'])
@renderer_classes([TemplateHTMLRenderer])
def myFriendFeed(request, friendID):

    user = Users.objects.get(id=friendID)
    posts = Posts.objects.filter(by=user).order_by("-upload_date")

    data = {
        "userFriend": user,
        "userPosts": posts
    }
    
    return Response(data, template_name="components/forFriend/friendFeed.html")


@api_view(['get'])
def deletePost(request):
    location = request.query_params.get("loc")
    pid = request.query_params.get("pid")
    post = get_object_or_404(Posts, id=pid)
    
    if post:
        post.delete()
        
    if location == "home":
        return redirect("/api/feedPage")
    elif location == "myPosts":
        return redirect("/api/myPosts")
    
    return Response({"error": "Not Allowed"})


@api_view(['get'])
@renderer_classes([TemplateHTMLRenderer])
def myPosts(request):
    
    posts = Posts.objects.filter(by=request.user).order_by("-upload_date")

    data = {
        "myPosts": posts
    }
    return Response(data, template_name="components/forPosts/myPosts.html")


@api_view(['get'])
@renderer_classes([TemplateHTMLRenderer])
def getNotifications(request):
    
    notifications = Notifications.objects.filter(to=request.user).order_by("-created")
    pages = Paginator(notifications, 2)
    page = request.query_params.get("page")
    if not page:
        page = 1
    
    data = {
        "notifications": pages.page(page)
    }
    
    return Response(data, template_name="components/notifications.html")


@api_view(['get'])
def read_notification(request):
    # Notification Id
    not_id = request.query_params.get("notId")
    page = request.query_params.get("page")
    obj = Notifications.objects.get(id=not_id)
    obj.isread = True
    post_id = obj.forPost.id
    obj.save()

    url = "/api/fullPost/?pid={0}&back=notifications&divId=main-Space".format(post_id)
    if page:
        url += "&page={0}".format(page)
        
    return redirect(url)


@api_view(['get'])
def readAllNots(request):
    
    notifications = Notifications.objects.filter(to=request.user, isread=False)
    for notif in notifications:
        notif.isread = True
        notif.save()
        
    
    return redirect("/api/getNots")

     
class HomeView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "components/homePage/feedPage.html"
    
    def get(self, request, format=None):
        friends = request.user.friends()
        query = Q(by__in=friends) | Q(by=request.user)

        post = Posts.objects.filter(query).order_by("-upload_date")
        data = {
            "post": post
        }
        
        return Response(data)
    
    def post(self, request, format=None):
        text = request.POST["post_text"]
        files = request.FILES.getlist("pics")

        post = Posts.objects.create(by=request.user)
        post.post_text = text
        path = ""
        urls = {
            "urls" : []
        }
        
        for file in files:   
            path, url = upload_post_pics(file, request.user.id, post.id)
            url = "http://" + str(request.META["HTTP_HOST"]) + "/" + url
            urls["urls"].append(url)

        post.urls = urls
        post.pics_path = path
        post.save()

        return redirect("/api/feedPage")
    

class UserView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "components/forAccount/account.html"
    
    def get(self, request, format=None):
        initials = {
            "username": request.user,
            "firstname": request.user.firstname,
            "lastname": request.user.lastname,
        }
        form = ChangeUserForm(label_suffix=" :: ", initial=initials)
        data = {
            "form": form,
            "type": 0
        }
        
        return Response(data)
    
    def post(self, request, format=None):
        form_data = {
            "username": request.user.username,
            "firstname": request.POST["firstname"],
            "lastname": request.POST["lastname"]
        }
        form = ChangeUserForm(form_data, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("/api/myAccount")
        
        return Response(form.errors.as_text())
    
    
class CommentView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "components/forComments/showComments.html"
    
    def post(self, request, format=None):
        data = request.data
        newComment = {
            "forPost": Posts.objects.get(id=data["post"]),
            "user": request.user,
            "comment": data["commentArea"],
            "reply": Comments.objects.get(id=data["forComment"]) if data["forComment"] != '0' else None
        }
        comment = Comments(**newComment)
        comment.save()
        context = {
            "posts": Posts.objects.get(id=comment.forPost.id)
        }
        return Response(context)
    
    def delete(self, request, cid):
        comment = Comments.objects.get(id=cid)
        context = {
            "posts": comment.forPost
        }
        comment.delete()
        
        return Response(context)