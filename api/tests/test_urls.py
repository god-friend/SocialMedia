from django.test import TestCase
from django.urls import resolve, reverse


from api.views import UserView, accountPage
from api.views import HomeView, uploadPage
from api.views import showProfilePics, showPostPics, deletePics
from api.views import showfullpost
from api.views import searchPage, searchUsers
from api.views import CommentView, likePost
from api.views import sendRequest, delRequest, requestPage, acceptRequest
from api.views import showFriends, unfriendUsers, myFriendFeed
from api.views import deletePost, myPosts
from api.views import getNotifications, read_notification, readAllNots


class TestUrls(TestCase):

    def setUp(self):
        self.message = "{0},URL test,Passed OK..."
        
        
    def test_url_feedPage(self):
        feedPage = reverse("api:homeView")        
        self.assertEquals(resolve(feedPage).func.view_class, HomeView)
        print(self.message.format("api/feedPage/"))
        
    def test_url_accountPage(self):
        account = reverse("api:accountPage")
        self.assertEquals(resolve(account).func, accountPage)
        print(self.message.format("api/account/"))

    def test_url_myAccount(self):
        myAccount = reverse("api:userView")
        self.assertEquals(resolve(myAccount).func.view_class, UserView)
        print(self.message.format("api/myAccount/"))
        
    def test_url_uploads(self):
        uploads = reverse("api:uploadPage")
        self.assertEquals(resolve(uploads).func, uploadPage)
        print(self.message.format("api/uploads/"))
        
    def test_url_proPics(self):
        proPics = reverse("api:profilePics")
        self.assertEquals(resolve(proPics).func, showProfilePics)
        print(self.message.format("api/proPics/"))
        
    def test_url_postPics(self):
        postPics = reverse("api:postPics")
        self.assertEquals(resolve(postPics).func, showPostPics)
        print(self.message.format("api/postPics/"))
        
    def test_url_deletePics(self):
        delete_pics = reverse("api:deletePics")
        self.assertEquals(resolve(delete_pics).func, deletePics)
        print(self.message.format("api/deletePics/"))
        
    def test_url_deletePost(self):
        delete_post = reverse("api:deletePost")
        self.assertEquals(resolve(delete_post).func, deletePost)
        print(self.message.format("api/deletePost/"))
        
    def test_url_fullPost(self):
        fullPost = reverse("api:fullPost")
        self.assertEquals(resolve(fullPost).func, showfullpost)
        print(self.message.format("api/fullPost/"))
        
    def test_url_myPosts(self):
        my_posts = reverse("api:myPosts")
        self.assertEquals(resolve(my_posts).func, myPosts)
        print(self.message.format("api/myPosts/"))

    def test_url_likePost(self):
        like_post = reverse("api:likePost", args=[1])
        self.assertEquals(resolve(like_post).func, likePost)
        print(self.message.format("api/likePost/<int:requestType>/"))
        
    def test_url_postComment(self):
        postComment = reverse("api:postComment")
        self.assertEquals(resolve(postComment).func.view_class, CommentView)
        print(self.message.format("api/postComment/"))
        
    def test_url_delComment(self):
        delComment = reverse("api:delComment", args=[10])
        self.assertEquals(resolve(delComment).func.view_class, CommentView)
        print(self.message.format("api/delComment/<int:cid>/"))
        
    def test_url_searchPage(self):
        search_page = reverse("api:searchPage")
        self.assertEquals(resolve(search_page).func, searchPage)
        print(self.message.format("api/searchPage/"))
        
    def test_url_searchUsers(self):
        search_users = reverse("api:searchUsers")
        self.assertEquals(resolve(search_users).func, searchUsers)
        print(self.message.format("api/searchUsers/"))
        
    def test_url_sendRequest(self):
        send_request = reverse("api:sendRequest", args=[1])
        self.assertEquals(resolve(send_request).func, sendRequest)
        print(self.message.format("api/sendRequest/<int:toUser>/"))
        
    def test_url_delRequest(self):
        del_request = reverse("api:delRequest", args=[1,2])
        self.assertEquals(resolve(del_request).func, delRequest)
        print(self.message.format("api/delRequest/<int:byUser>/<int:toUser>/"))
        
    def test_url_requestPage(self):
        request_page = reverse("api:requestPage")
        self.assertEquals(resolve(request_page).func, requestPage)
        print(self.message.format("api/requestPage/"))
        
    def test_url_acceptRequest(self):
        accept_request = reverse("api:acceptRequest", args=[21])
        self.assertEquals(resolve(accept_request).func, acceptRequest)
        print(self.message.format("api/acceptRequest/<int:by>/"))
        
    def test_url_myFriends(self):
        myFriends = reverse("api:showFriends")
        self.assertEquals(resolve(myFriends).func, showFriends)
        print(self.message.format("api/myFriends/"))
        
    def test_url_unfriend(self):
        unfriend = reverse("api:unfriendUsers")
        self.assertEquals(resolve(unfriend).func, unfriendUsers)
        print(self.message.format("api/unfriend/"))
        
    def test_url_friendFeed(self):
        friendFeed = reverse("api:myFriendFeed", args=[1])
        self.assertEquals(resolve(friendFeed).func, myFriendFeed)
        print(self.message.format("api/friendFeed/"))
        
    def test_url_getNots(self):
        getNots = reverse("api:getNots")
        self.assertEquals(resolve(getNots).func, getNotifications)
        print(self.message.format("api/getNots/"))
        
    def test_url_readNotification(self):
        readNotification = reverse("api:readNotification")
        self.assertEquals(resolve(readNotification).func, read_notification)
        print(self.message.format("api/readNotification/"))
        
    def test_url_readAllNots(self):
        read_all_nots = reverse("api:readAllNots")
        self.assertEquals(resolve(read_all_nots).func, readAllNots)
        print(self.message.format("api/readAllNots/"))
    
        

