from django.test import TestCase, Client
from django.urls import reverse
from django.core.files import File
from django.core.paginator import UnorderedObjectListWarning

from rest_framework.status import HTTP_200_OK, HTTP_302_FOUND, HTTP_403_FORBIDDEN

from main.models import Users, Posts, Likes, Comments, Requests, Friends, Notifications
from main.extras import upload_post_pics

import warnings
warnings.simplefilter("ignore", category=UnorderedObjectListWarning)



class CommonFuncs(TestCase):
    
    def setUp(self):
        self.user = Users.objects.create_user(username="testuser", password="Testuser@123")
        
        self.loggedInClient = Client()
        self.loggedInClient.login(username=self.user.username,password="Testuser@123")
        self.anonymousUser = Client()
    
    def getRequest(self, page, template, authStatus, pageURL, getData=None, **kwargs):
        anonStatus = kwargs.get("anonStatus") if kwargs.get("anonStatus") else HTTP_403_FORBIDDEN 
        anonTemp = kwargs.get("anonTemp") if kwargs.get("anonTemp") else None
        
        # User Logged in
        loginResponse = self.loggedInClient.get(page, getData)

        self.assertEquals(loginResponse.status_code, authStatus)
        if template:
            self.assertTemplateUsed(loginResponse, template)
            print("Authorized User,GET,{0},{1},{2},Passed OK..".format(template, authStatus, pageURL))    
        else:
            print("Authorized User,GET,redirected,{0},{1},Passed OK..".format(authStatus, pageURL))
        
        # User not Logged In
        anonymousResponse = self.anonymousUser.get(page)
                
        self.assertEqual(anonymousResponse.status_code, anonStatus)
        if anonTemp:
            self.assertTemplateUsed(anonymousResponse, anonTemp)
            print("Unauthorized User,GET,{0},{1},{2},Passed OK..".format(anonTemp, anonStatus, pageURL)) 
        else:
            if anonStatus == HTTP_302_FOUND:
                print("Unauthorized User,GET,redirected,{0},{1},Passed OK..".format(anonStatus, pageURL))
            elif anonStatus == HTTP_403_FORBIDDEN:
                print("Unauthorized User,GET,None,{0},{1},Passed OK..".format(anonStatus, pageURL)) 
        
    def postRequest(self, page, authStatus, pageURL, postData, template=None, **kwargs):
        anonStatus = kwargs.get("anonStatus") if kwargs.get("anonStatus") else HTTP_403_FORBIDDEN 
        anonTemp = kwargs.get("anonTemp") if kwargs.get("anonTemp") else None
        anonPostData = kwargs.get("anonPost") if kwargs.get("anonPost") else None
        
        # User Logged in
        loginResponse = self.loggedInClient.post(page, data=postData)    
        
        self.assertEquals(loginResponse.status_code, authStatus)
        if template:
            self.assertTemplateUsed(loginResponse, template)
            print("Authorized User,POST,{0},{1},{2},Passed OK..".format(template, authStatus, pageURL))
        else:
            print("Authorized User,POST,redirected,{0},{1},Passed OK..".format(authStatus, pageURL))
        
        # User Not Logged in
        anonymousResponse = self.anonymousUser.post(page, anonPostData)
        self.assertEqual(anonymousResponse.status_code, anonStatus)
        if anonTemp:
            self.assertTemplateUsed(anonymousResponse, anonTemp)
            print("Unauthorized User,POST,{0},{1},{2},Passed OK..".format(anonTemp, anonStatus, pageURL))
        else:
            if anonStatus == HTTP_302_FOUND:
                print("Unauthorized User,POST,redirected,{0},{1},Passed OK..".format(anonStatus, pageURL))
            elif anonStatus == HTTP_403_FORBIDDEN:
                print("Unauthorized User,POST,None,{0},{1},Passed OK..".format(anonStatus, pageURL))
    
    def createPostObject(self):
        post = Posts.objects.create(by=self.user)
        post.post_text="Hey"
        urls = {
            "urls": []
        }
        file = File(open("/home/god-friend/Documents/abstract-5719221_1280.jpg","rb"))
        path, url = upload_post_pics(file, self.user.id, post.id)
        urls["urls"].append(url)
        post.urls = urls
        post.pics_path = path
        post.save()
        return post

    def createLiked(self, post):
        likes = Likes.objects.create(byUser=self.user, likedPost=post)
        
        return likes
    
    def createComment(self, post, reply=None):
        commentData = {
            "forPost": post,
            "user": self.user,
            "comment": "test",
            "reply": reply
        }
        comment = Comments(**commentData)
        comment.save()
        return comment
        
    def createRequest(self):
        user = Users.objects.create_user(username="test2", password="test2@123")
        req = Requests.objects.create(by=user, to=self.user)
        
        return req
    
    def createFriend(self):
        user = Users.objects.create_user(username="test2", password="test2@123")
        friend = Friends.objects.create(user=self.user, friend=user)
        
        return friend
    
    def createNotification(self, post):
        noti = Notifications.objects.create(to=self.user, forPost=post, notification="test")
        
        return noti



class ViewsTest(CommonFuncs):
    
    def test_template_feedPage(self):
        feedPage = reverse("api:homeView")
        postData = {
            "post_text": "Hello World",
        }
        self.getRequest(feedPage, "components/homePage/feedPage.html",
                        HTTP_200_OK, "/api/feedPage/")
        
        self.postRequest(feedPage, HTTP_302_FOUND, "/api/feedPage/", postData)
        
    def test_template_account(self):
        accountPage = reverse("api:accountPage")
        self.getRequest(accountPage, "components/forAccount/account_page.html",
                     HTTP_200_OK, "/api/account/")        
        
    def test_template_myAccount(self):
        myAccount = reverse("api:userView")
        postData = {
            "firstname": "test",
            "lastname": "user"
        }
        self.getRequest(myAccount, "components/forAccount/account.html",
                        HTTP_200_OK, "/api/myAccount/")
        self.postRequest(myAccount, HTTP_302_FOUND, "/api/myAccount/", postData)
        
    def test_template_uploads(self):
        uploads = reverse("api:uploadPage")
        self.getRequest(uploads, "components/forUploads/uploads.html",
                     HTTP_200_OK, "/api/uploads/")
    
    def test_template_proPics(self):
        proPics = reverse("api:profilePics")
        self.getRequest(proPics, "components/forUploads/showPrPics.html",
                        HTTP_200_OK, "/api/proPics/")
        
    def test_template_postPics(self):
        postPics = reverse("api:postPics")
        self.getRequest(postPics, "components/forUploads/showPrPics.html",
                        HTTP_200_OK, "/api/postPics/")
        
    def test_template_deletePics(self):
        deletePics = reverse("api:deletePics")
        self.user.profile_pic.save(name="dpImg.png",content= 
        File(open("/home/god-friend/Documents/abstract-5719221_1280.jpg", "rb")))
        getData = {
            "dpPath": self.user.profile_pic.url
        }
        self.getRequest(deletePics, None, HTTP_302_FOUND, "/api/deletePics/?dpPath=''", getData)
        
        post = self.createPostObject()
        getData2 = {
            "pPath": post.urls["urls"][0]
        }
        self.getRequest(deletePics, None, HTTP_302_FOUND, "/api/deletePics/?pPath=''", getData2)
        post.delete()
        
    def test_template_deletePost(self):
        deletePost = reverse("api:deletePost")
        post = self.createPostObject()
        getData = {
            "loc": "home",
            "pid": post.id
        }
        self.getRequest(deletePost, None, HTTP_302_FOUND, "/api/deletePost/?loc=home&pid=''", getData)
        
        post2 = self.createPostObject()
        getData["loc"] = "myPosts"
        getData["pid"] = post2.id
        self.getRequest(deletePost, None, HTTP_302_FOUND, "/api/deletePost/?loc=myPosts&pid=''", getData)
        
    def test_template_fullPost(self):
        fullPost = reverse("api:fullPost")
        post = self.createPostObject()
        getData = {
            "back": "home",
            "divId": "main-Space",
            "pid": post.id
        }
        self.getRequest(fullPost, "components/forPosts/full_post.html",
                        HTTP_200_OK, "/api/fullPost/?pid=''&back=''&divId=''", getData)    
        
        post.delete()
  
    def test_template_myPosts(self):
        myPosts = reverse("api:myPosts")
        self.getRequest(myPosts, "components/forPosts/myPosts.html", HTTP_200_OK, "/api/myPosts/")
          
    def test_template_likePost(self):
        likePost = reverse("api:likePost", args=[1])
        post = self.createPostObject()
        likes = self.createLiked(post)
        getData = {
            "postId": post.id,
            "pageType": "fullPage"
        }
        self.getRequest(likePost, None, HTTP_302_FOUND, 
                        "/api/likePost/0/?pageType='fullPage'&postId=''", getData)
        getData["pageType"] = "feedPage"
        likes = self.createLiked(post)
        self.getRequest(likePost, "components/forPosts/post.html", HTTP_200_OK,
                        "/api/likePost/1/?pageType='home'&postId=''", getData)
        post.delete()
    
    def test_template_postComment(self):
        postComment = reverse("api:postComment")
        post = self.createPostObject()
        postData = {
            "post": post.id,
            "commentArea": "test",
            "forComment": 0
        }
        self.postRequest(postComment, HTTP_200_OK, 
        "/api/postComment/", postData, "components/forComments/showComments.html")
        post.delete()
        
    def test_template_delComment(self):
        post = self.createPostObject()
        comment = self.createComment(post)
        delComment = reverse("api:delComment", args=[comment.id])
        
        response = self.loggedInClient.delete(delComment)
        template = "components/forComments/showComments.html"
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTemplateUsed(response, template)
        print("Authorized User,DELETE,{0},{1},{2}, Passed OK..".format(template,HTTP_200_OK, "/api/delComment/cid"))
        
        response1 = self.anonymousUser.delete(delComment)
        
        self.assertEqual(response1.status_code, HTTP_403_FORBIDDEN)
        print("Unauthorized User,DELETE,None,{0}, {1}, Passed OK..".format(HTTP_403_FORBIDDEN, "/api/delComment/cid"))
        post.delete()
        
    def test_template_searchPage(self):
        searchPage = reverse("api:searchPage")
        self.getRequest(searchPage, "components/forSearch/searchPage.html", HTTP_200_OK,
                        "/api/searchPage/")
        
    def test_template_searchUsers(self):
        searchUsers = reverse("api:searchUsers")
        getData = {
            "find": "n",
            "page": 1
        }
        self.getRequest(searchUsers, "components/forSearch/searchResults.html", HTTP_200_OK,
                        "/api/searchUsers/", getData)
        
    def test_template_sendRequest(self):
        sendRequest = reverse("api:sendRequest", args=[1])
        getData = {
            "page": 1,
            "find": "n"
        }
        self.getRequest(sendRequest, None, HTTP_302_FOUND, 
                        "/api/sendRequest/<toUser>/?page=''&find=''",getData)
    
    def test_template_delRequest(self):
        req = self.createRequest()
        delRequest = reverse("api:delRequest", args=[req.by.id, req.to.id])
        
        self.getRequest(delRequest, None,
                        HTTP_302_FOUND, "/api/delRequest/byUser/toUser")
    
    def test_template_requestPage(self):
        requestPage = reverse("api:requestPage")
        self.getRequest(requestPage, "components/forRequest/requests.html",
                        HTTP_200_OK, "/api/requestPage/")
        
    def test_template_acceptRequest(self):
        req = self.createRequest()
        acceptRequest = reverse("api:acceptRequest", args=[req.by.id])
        
        self.getRequest(acceptRequest, None,
                        HTTP_302_FOUND, "/api/acceptRequest/<byUser>/")
        
    def test_template_myFriends(self):
        myFriends = reverse("api:showFriends")
        self.getRequest(myFriends, "components/forFriend/friends.html", 
                        HTTP_200_OK, "/api/myFriends/")
        
    def test_template_unfriend(self):
        unfriend = reverse("api:unfriendUsers")
        friend = self.createFriend()
        getData = {
            "userId": self.user.id,
            "friendId": friend.friend.id
        }
        self.getRequest(unfriend, None, HTTP_302_FOUND,
                        "/api/unfriend/", getData)
        
    def test_template_friendFeed(self):
        friend = self.createFriend()
        friendFeed = reverse("api:myFriendFeed", args=[friend.friend.id])
        
        self.getRequest(friendFeed, "components/forFriend/friendFeed.html",
                        HTTP_200_OK, "/api/friendFeed/friendId/")
        
    def test_template_getNots(self):
        getNots = reverse("api:getNots")
        self.getRequest(getNots, "components/notifications.html", HTTP_200_OK,
                        "/api/getNots/")
        
    def test_template_readNotification(self):
        readNotification = reverse("api:readNotification")
        post = self.createPostObject()
        noti = self.createNotification(post)
        getData = {
            "notId": noti.id
        }
        self.getRequest(readNotification, None, HTTP_302_FOUND,
                        "/api/readNotification/", getData)
        post.delete()
        
    def test_template_readAllNots(self):
        readAllNots = reverse("api:readAllNots")
        post = self.createPostObject()
        noti = self.createNotification(post)
        self.getRequest(readAllNots, None, HTTP_302_FOUND,
                        "/api/readAllNots/")
        post.delete()
    
        
    