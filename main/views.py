from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth import login, logout
from django.db.models import Q

from .forms import LoginForm, CreateUserForm, ChangeUserForm

from .models import Posts, Comments, Requests, Friends, Notifications
from .extras import upload_post_pics, get_all_profile_pics, delProfilePic
from .models import Users

def sign_out(request):
    if request.method == "GET":
        logout(request)
        return redirect("/")
    return HttpResponse("Method Not Allowed")

class LoginUser(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home/")
        
        data = {
            "form": LoginForm()
        }
        return render(request, "auth/login.html", data)
    
    def post(self, request):
        if not request.user.is_authenticated:
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect("home/")
            data = {
                "form": form,
            }
            return render(request, "auth/login.html", data)
        
        return redirect("home/")

class NewUser(View):

    def get(self, request):
        if not request.user.is_authenticated:
            data = {
                "form": CreateUserForm()
            }
            return render(request, "auth/signup.html", data)

        return redirect("home/")

    def post(self, request):
        if not request.user.is_authenticated:
            form = CreateUserForm(data=request.POST)

            if form.is_valid():
                form.save()
                return redirect("/")

            data = {
                "form": form,
            }
            return render(request, "auth/signup.html", data)

        return redirect("home/")    

class HomeView(View):

    def get(self, request, home=None):
        if not request.user.is_authenticated:
            return redirect("/")
        
        friends = request.user.friends()
        query = Q(by__in=friends) | Q(by=request.user)
        # print(list(friends))
        post = Posts.objects.filter(query).order_by("-upload_date")
        data = {
            "post": post
        }
        # print(request.GET)
        if not home:
            return render(request, "main_app/index.html", data)
        return render(request, "components/homePage/feedPage.html", data)
    

    def post(self, request):

        if not request.user.is_authenticated:
            return HttpResponse("Method Not Allowed")
        
        text = request.POST["post_text"]
        files = request.FILES.getlist("pics")
        # print(text, files)
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

        return redirect('/home/1')
    
class UserAccount(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("/")
        
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
        return render(request, "components/forAccount/account_page.html", data)
    
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("/")
        
        form_data = {
            "username": request.user.username,
            "firstname": request.POST["firstname"],
            "lastname": request.POST["lastname"]
        }
        form = ChangeUserForm(form_data, request.FILES, instance=request.user)
        # print(form)
        if form.is_valid():
            form.save()
            return redirect("/account")
        
        return HttpResponse(form.errors.as_text())

class UserUploads(View):

    def get(self, request, show):
        if not request.user.is_authenticated:
            return redirect("/")
        
        data = {}
        if show == 0:
            # Show the Latest Profile pic and Post Pic Uploaded
            latestPost = Posts.objects.filter(by=request.user).exclude(urls__urls__iexact="[]").last()
            if not latestPost:
                lUrl = None
            else:
                lUrl = latestPost.urls["urls"][0]

            pPic = request.user.profile_pic
            if pPic:
                pPic = request.user.profile_pic.url
            # print(latestPost)
            data = {
                "type": 1,
                "profile": pPic,
                "postPics": lUrl
            }
            return render(request, "components/forAccount/account_page.html", data)
        elif show == 1:
            # Show All Profile Pics Uploaded Till Date
            if request.user.profile_pic:
                userProPics = request.user.profile_pic.url
                indx = userProPics.rfind("/")
                indxs = userProPics.find("/", userProPics.find("/")+1)
                url = userProPics[:indx+1]
                allProfilePics = get_all_profile_pics(userProPics[indxs:indx])
                allProfilePicsUrl = [(url+pName) for pName in allProfilePics]
                pages = Paginator(allProfilePicsUrl, 2)
                page = request.GET.get("page")
                if(page == None):
                    page = 1 

                data = {
                    "type": 10,
                    "pPics": pages.page(page),
                    "total_pages": pages.page_range,
                }
                return render(request, "components/forAccount/account_page.html", data)
            else:
                return redirect("/uploads/0/")
        elif show == 2:
            # Show All pics Uploaded By user at Feed
            posts = Posts.objects.filter(by=request.user)
            urls = []
            for x in posts:
                urls += x.urls["urls"]

            pages = Paginator(urls, 2)
            page = request.GET.get("page")
            if(page == None):
                page = 1

            data = {
                "type": 11,
                "pPics": pages.page(page),
                "total_pages": pages.page_range
            }
            return render(request, "components/forAccount/account_page.html", data)
        return HttpResponse("Not Allowed")

def show_full_post(request, pid):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if request.method == "GET":
        post = Posts.objects.get(id=pid)

        data = {
            "posts": post
        }

        return render(request, "components/forPosts/full_post.html", data)
        # return HttpResponse("Okay")
    
    return HttpResponse("Method Not Allowed")
        
def comment_on_post(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("/")
        
        data = request.POST
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
        return render(request, "components/forComments/showComments.html", context)

    return HttpResponse("Method Not Allowed")

def delete_comment(request, cid):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect("/")
        
        comment = Comments.objects.get(id=cid)
        context = {
            "posts": comment.forPost
        }
        comment.delete()
        return render(request, "components/forComments/showComments.html", context)


    return HttpResponse("Method Not Allowed")

def search_users(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect("/")
        
        find = request.GET.get("find")
        current_user = request.user
        
        query = (Q(firstname__contains=find) | Q(lastname__contains=find)) & ~Q(username=current_user)
        exQuery = Q(id__in=current_user.friends().values("friend_id")) | Q(id__in=current_user.friends().values("user_id"))
        
        users = Users.objects.filter(query).exclude(exQuery)
        
        pages = Paginator(users, 1)
        page = request.GET.get("page")
        if not page:
            page = 1
        elif int(page) > pages.num_pages:
            page = pages.num_pages

        data = {
            "results": pages.page(page),
            "query": find
        }
        return render(request, "components/searchResults.html", data)
    
    return HttpResponse("Method Not Allowed")

def send_request(request, to, query, page):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect("/")
        
        user = Users.objects.get(id=to)
        req = Requests(by=request.user, to=user)
        req.save()

        return redirect("/search/?find={0}&page={1}".format(query, page))

    return HttpResponse("Method Not Allowed")

def cancel_request(request, to, query=None, page=None):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect("/")
        
        user = Users.objects.get(id=to)
        req = Requests.objects.get(by=request.user, to=user)
        req.delete()
        if not query and not page:
            return redirect("/requests/")

        return redirect("/search/?find={0}&page={1}".format(query, page))

    return HttpResponse("Method Not Allowed")

def getR(request):

    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect("/")
        
        got_requests = Requests.objects.filter(to=request.user)
        sended_request = Requests.objects.filter(by=request.user)
        # print(sended_request)

        data = {
            "got_requests": got_requests,
            "sended_requests": sended_request
        }

        return render(request, "components/forRequest/requests.html", data)
    
    return HttpResponse("Method Not Allowed")

def acceptR(request, by, query=None, page=None):

    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect("/")
        
        rObj = Requests.objects.get(by=by, to=request.user)
        rObj.delete()
        requestSendedBy = Users.objects.get(id=by)

        makeFriend = Friends.objects.create(user=requestSendedBy, friend=request.user)
        if not query and not page:
            return redirect("/requests/")
        
        return redirect("/search/?find={0}&page={1}".format(query, page))
    
    return HttpResponse("Method Not Allowed")

def rejectR(request, by, query=None, page=None):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect("/")
        
        rObj = Requests.objects.get(by=by, to=request.user)
        rObj.delete()

        if not query and not page:
            return redirect("/requests/")
        
        return redirect("/search/?find={0}&page={1}".format(query, page))
    
    return HttpResponse("Method Not Allowed")

def get_notifications(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect("/")
        
        notifications = Notifications.objects.filter(to=request.user).order_by("-created")
        pages = Paginator(notifications, 2)
        page = request.GET.get("page")
        if not page:
            page = 1
        
        # print(request.META)
        data = {
            "notifications": pages.page(page)
        }

        return render(request, "components/notifications.html", data)
    return HttpResponse("Method Not Allowed")
    
def read_notification(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect("/")
        # Notification Id
        not_id = request.GET.get("notId")

        obj = Notifications.objects.get(id=not_id)
        obj.isread = True
        post_id = obj.forPost.id
        obj.save()

        return redirect("/post/{0}".format(post_id))
    
    return HttpResponse("Method Not Allowed")

def showFriends(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect("/")
        
        friends_id = request.user.friends()
        print(friends_id)
        query = Q(id__in=friends_id)
        friends = Users.objects.filter(query)
        pages = Paginator(friends, 2)
        page = request.GET.get("page")
        if not page:
            page = 1

        data = {
            "friends": pages.page(page)
        }

        return render(request, "components/forFriend/friends.html", data)

    return HttpResponse("Method Not Allowed")

def showFriendFeed(request, friend):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect("/")
        
        user = Users.objects.get(id=friend)
        posts = Posts.objects.filter(by=friend).order_by("-upload_date")

        data = {
            "userFriend": user,
            "userPosts": posts
        }

        return render(request, "components/forFriend/friendFeed.html", data)

    return HttpResponse("Method Not Allowed")

def myPosts(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect("/")
        posts = Posts.objects.filter(by=request.user).order_by("-upload_date")

        data = {
            "myPosts": posts
        }

        return render(request, "components/forPosts/myPosts.html", data)

    return HttpResponse("Method Not Allowed")

def deletePost(request, pid):
    
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect("/")
        
        
        loc = int(request.GET.get("loc"))
        post = get_object_or_404(Posts, id=pid)
        if post:
            post.delete()
        
        if loc == 1:
            return redirect("/myPosts/")
        return redirect("/home/1/")

    return HttpResponse("Method Not Allowed")

def deleteProfilePic(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect("/")

        loc = request.GET.get("pLoc")
        s = loc.find("dp")

        delProfilePic(loc[s:])
        user = Users.objects.get(id=request.user.id)

        end = loc.rfind("/")
        profilePics = get_all_profile_pics(loc[s-1:end+1])
        
        if len(profilePics) > 0:
            user.profile_pic = loc[s-1:end+1] + profilePics[0]
        else:
            user.profile_pic = None
        user.save()

        return redirect("/uploads/1/")

    return HttpResponse("Method Not Allowed")

def markAllNotifRead(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect("/")
        
        nots = Notifications.objects.filter(to=request.user)
        for x in nots:
            x.isread = True
            x.save()

        return redirect("/notifications")
    
    return HttpResponse("Method Not Allowed")