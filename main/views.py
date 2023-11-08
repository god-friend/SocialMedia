from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth import login, logout
from django.db.models import Q

from .forms import LoginForm, CreateUserForm

from .models import Posts, Requests, Notifications


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


def homePage(request):
    
    if not request.user.is_authenticated:
        return redirect("/")
    
    if request.method == "GET":
        friends = request.user.friends()
        query = Q(by__in=friends) | Q(by=request.user)
        post = Posts.objects.filter(query).order_by("-upload_date")
        data = {
            "pageType": "home",
            "post": post
        }
        return render(request, "main_app/index.html", data)
    
    return HttpResponse("Method Not Allowed")


def accountPage(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if request.method == "GET":
        data = {
            "pageType": "account",
        }
        return render(request, "main_app/index.html", data)

    return HttpResponse("Method Not Allowed")


def notificationPage(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if request.method == "GET":
        notifications = Notifications.objects.filter(to=request.user).order_by("-created")
        pages = Paginator(notifications, 2)
        page = 1
        
        data = {
            "pageType": "notify",
            "notifications": pages.page(page)
        }
        
        return render(request, "main_app/index.html", data)
    return HttpResponse("Method Not Allowed")


def requestsPage(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if request.method == "GET":
        got_requests = Requests.objects.filter(to=request.user)
        sended_request = Requests.objects.filter(by=request.user)

        data = {
            "pageType": "requests",
            "got_requests": got_requests,
            "sended_requests": sended_request
        }
        
        return render(request, "main_app/index.html", data)
    return HttpResponse("Method Not Allowed")


def searchPage(request):
    if not request.user.is_authenticated:
        return redirect("/")
    
    if request.method == "GET":
        data = {
            "pageType": "search"
        }
        return render(request, "main_app/index.html", data)
    return HttpResponse("Method Not Allowed")
