from django.urls import path

from .views import sign_out, LoginUser, NewUser
from .views import homePage, accountPage, notificationPage, requestsPage, searchPage

urlpatterns = [
    path('', LoginUser.as_view(), name="login"),
    path('create/', NewUser.as_view(), name="signup"),
    path('logout/', sign_out, name="logout"),
    path('home/', homePage, name="homePage"),
    path("account/", accountPage, name="accountPage"),
    path("notifications/", notificationPage, name="notifications"),
    path("requests/", requestsPage, name="requestsPage"),
    path("search/", searchPage, name="searchPage")
]
