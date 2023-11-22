from main.models import Users, Posts, Comments, Likes, Requests, Friends, Notifications

from django.db.models import Q

from api.tests.test_views_templates import CommonFuncs

message = "{0}, {1} returns {2}, Passed OK..."

class TestModels(CommonFuncs):
    
    def test_isStaff(self):
        obj = self.user.is_staff
        returns = self.user.isStaff()
        self.assertEquals(obj, returns)
        print(message.format("user","isStaff()", returns))
        
    def test_fullname(self):
        self.user.firstname = "test"
        self.user.lastname = "user"
        self.user.save()
        obj = self.user.firstname + " " + self.user.lastname
        returns = self.user.get_fullname()
        self.assertEquals(obj, returns)
        print(message.format("user","get_fullname()", returns))
        
    def test_friends(self):
        friend = self.createFriend()
        query = Friends.objects.filter(user=self.user).values_list("friend_id")
        q2 = Friends.objects.filter(friend=self.user).values_list("user_id").union(query)
        self.assertQuerySetEqual(self.user.friends(), q2)
        print(message.format("user","friends()", q2))
        
    def test_notificationCount(self):
        post = self.createPostObject()
        noti = self.createNotification(post)
        obj = Notifications.objects.filter(to=self.user, isread=False).count()
        returns = self.user.notify_count()
        self.assertEquals(obj, returns)
        print(message.format("user","notify_count()", returns))
        post.delete()
        
    def test_reqCount(self):
        obj = Requests.objects.filter(to=self.user).count()
        returns = self.user.request_count()
        self.assertEquals(obj, returns)
        print(message.format("user","request_count()", returns))
        
    def test_reqSended(self):
        obj = Requests.objects.filter(by=self.user)
        returns = self.user.request_sended()
        self.assertQuerySetEqual(obj, returns)
        print(message.format("user","request_sended()", returns))
        
    def test_areFriends(self):
        friend = self.createFriend()
        friendCount = Friends.objects.filter(user=self.user, friend=friend.friend).count()
        fCount = Friends.objects.filter(user=friend.friend, friend=self.user).count()
        count = friendCount + fCount
        obj = True if count >=1 else False
        returns = self.user.areFriends(friend.friend)
        self.assertEquals(obj, returns)
        print(message.format("user","areFriends(x)", returns))
        
    def test_get_comments(self):
        post = self.createPostObject()
        comment = self.createComment(post)
        obj = Comments.objects.filter(reply=None, forPost=post)
        returns = post.get_comments()
        self.assertQuerySetEqual(obj, returns)
        print(message.format("posts", "get_comments()", returns))
        
        post.delete()
        
    def test_isParent(self):
        post = self.createPostObject()
        comment = self.createComment(post)
        obj = Comments.objects.get(forPost=post, user=self.user)
        if obj.reply == None:
            obj = True
            
        returns = comment.isParent()
        self.assertEquals(obj, returns)
        print(message.format("comments", "isParent()", returns))
        post.delete()
        
    def test_allReplies(self):
        post = self.createPostObject()
        comment = self.createComment(post)
        comment2 = self.createComment(post, comment)
        obj = Comments.objects.filter(forPost=post, user=self.user, reply=comment)
            
        returns = comment.allReplies()
        self.assertQuerySetEqual(obj, returns)
        print(message.format("comments", "allReplies()", returns))
        post.delete()
        