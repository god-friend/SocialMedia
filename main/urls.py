from django.urls import path
from .views import sign_out, show_full_post, comment_on_post
from .views import delete_comment, search_users, send_request, cancel_request, getR
from .views import acceptR, rejectR, get_notifications, read_notification, showFriends
from .views import showFriendFeed, myPosts, deletePost
from .views import LoginUser, NewUser
from .views import HomeView, UserAccount, UserUploads


urlpatterns = [
    path('', LoginUser.as_view(), name="login"),
    
    path('create/', NewUser.as_view(), name="signup"),
    path('logout/', sign_out, name="logout"),
    
    path('home/', HomeView.as_view(), name="home"),
    path('home/<int:home>/', HomeView.as_view(), name="homeI"),
    
    path('account/', UserAccount.as_view(), name="account"),
    path('uploads/<int:show>/', UserUploads.as_view(), name="uploads"),
    
    path('post/<int:pid>/', show_full_post, name="fullPost"),
    
    path('comment/', comment_on_post, name='comment'), 
    path('cDel/<int:cid>', delete_comment, name="cDel"),
    
    path('search/', search_users, name="search"),
    
    path('sReq/<int:to>/<str:query>/<int:page>', send_request, name="sReq"),
    
    path('cReq/<int:to>/', cancel_request, name="cReq"),
    path('cReq/<int:to>/<str:query>/<int:page>', cancel_request, name="cReq1"),
    
    path("requests/", getR, name="requests"),
    
    path("acceptR/<int:by>/", acceptR, name="acceptRequest"),
    path("acceptR/<int:by>/<str:query>/<int:page>", acceptR, name="acceptRequest1"),
    
    path("rejectR/<int:by>/", rejectR, name="rejectRequest"),
    path("rejectR/<int:by>/<str:query>/<int:page>", rejectR, name="rejectRequest1"),

    path("notifications/", get_notifications, name="notifications"),
    path("readNot/", read_notification, name="read_not"),

    path("friends/", showFriends, name="friends"),
    path("fFeed/<int:friend>/", showFriendFeed, name="fFeed"),

    path("myPosts/", myPosts, name="mPosts"),
    
    path("deletePosts/<int:pid>/", deletePost, name="deletePosts")
]
