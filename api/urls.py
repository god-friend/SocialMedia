from django.urls import path

from .views import UserView, accountPage
from .views import HomeView, uploadPage
from .views import showProfilePics, showPostPics, deletePics
from .views import showfullpost
from .views import searchPage, searchUsers
from .views import CommentView
from .views import sendRequest, delRequest, requestPage, acceptRequest
from .views import showFriends, unfriendUsers, myFriendFeed
from .views import deletePost, myPosts
from .views import getNotifications, read_notification, readAllNots

urlpatterns = [
    path("feedPage/", HomeView.as_view(), name="homeView"),
    path('account/', accountPage, name="accountPage"),
    path('myAccount/', UserView.as_view(), name='userView'),
    path('uploads/', uploadPage, name="uploadPage"),
    path('proPics/', showProfilePics, name="profilePics"),
    path('postPics/', showPostPics, name="postPics"),
    path('deletePics/', deletePics, name="deletePics"),
    path('deletePost/', deletePost, name="deletePost"),
    path('fullPost/', showfullpost, name="fullPost"),
    path('myPosts/', myPosts, name="myPosts"),
    path('postComment/', CommentView.as_view(), name="postComment"),
    path('delComment/<int:cid>', CommentView.as_view(), name="delComment"),
    path('searchPage/', searchPage, name="searchPage"),
    path('searchUsers/', searchUsers, name="searchUsers"),
    path('sendRequest/<int:toUser>/', sendRequest, name="sendRequest"),
    path('delRequest/<int:byUser>/<int:toUser>/', delRequest, name="delRequest"),
    path('requestPage/', requestPage, name="requestPage"),
    path('acceptRequest/<int:by>/', acceptRequest, name="acceptRequest"),
    path('myFriends/', showFriends, name="showFriends"),
    path('unfriend/', unfriendUsers, name="unfriendUsers"),
    path('friendFeed/<int:friendID>', myFriendFeed, name="myFriendFeed"),
    path('getNots/', getNotifications, name="getNots"),
    path('readNotification/', read_notification, name="readNotification"),
    path('readAllNots/', readAllNots, name="readAllNots")
    
]