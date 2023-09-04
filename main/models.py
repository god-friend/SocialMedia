from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UsersManager
from django.db import models
from .extras import upload_profile_pic
from django.db.models import Q

class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name="Username", max_length=256, unique=True, help_text="Username Must be Lowercase alphabets")
    firstname = models.CharField(max_length=256)
    lastname = models.CharField(max_length=256)
    profile_pic = models.FileField(upload_to=upload_profile_pic)
    last_login = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UsersManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    
    def has_perm(self, perm, obj=None):
        return True
    
    def isStaff(self):
        return self.is_staff
    
    def __str__(self):
        return "{0}".format(self.username)
    
    def get_fullname(self):
        return self.firstname + " " + self.lastname
    
    def friends(self):
        # f = Q(user=self) | Q(friend=self)
        queryset = self.friendOf.filter(user=self).values_list("friend_id")
        q2 = self.friend.filter(friend=self).values_list("user_id").union(queryset)
        return q2
    
    def notify_count(self):
        count = self.notifications.filter(to=self, isread=False).count()
        return count

    def request_count(self):
        count = self.requested.filter(to=self).count()
        return count
    
    def request_sended(self):
        requests = self.request.filter(by=self)
        return requests
    
    def areFriends(self,x):
        frcount = self.friendOf.filter(user=self, friend=x).count()
        fcount = self.friend.filter(friend=self, user=x).count()
        count = frcount + fcount
        print(count)
        if count >= 1:
            return True
        return False


class Posts(models.Model):
    by = models.ForeignKey(Users, on_delete=models.CASCADE)
    post_text = models.CharField(max_length=1024)
    pics_path = models.CharField(max_length=1024, default="")
    upload_date = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)
    urls = models.JSONField(default=dict)
    likes = models.IntegerField(default=0)


    def __str__(self) -> str:

        return "post_{0} by {1}".format(self.id, self.by.username)
    

    def get_comments(self):
        return self.comment.filter(reply=None)
    

class Comments(models.Model):
    forPost = models.ForeignKey("Posts", on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey("Users", on_delete=models.CASCADE, related_name="byUser")
    created = models.DateField(auto_now_add=True)
    comment = models.CharField(max_length=256)
    reply = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")

    def __str__(self):
        return self.comment
    
    def isParent(self):
        if self.reply is None:
            return True
        return False
    
    def allReplies(self):
        return Comments.objects.filter(reply=self)
    

class Friends(models.Model):
    user = models.ForeignKey("Users", on_delete=models.CASCADE, related_name="friendOf")
    friend = models.ForeignKey("Users", on_delete=models.CASCADE, related_name="friend")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.friend.username
    
class Requests(models.Model):
    by = models.ForeignKey("Users", on_delete=models.CASCADE, related_name="request")
    to = models.ForeignKey("Users", on_delete=models.CASCADE, related_name="requested")
    onDate = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.to.username
    

class Notifications(models.Model):
    to = models.ForeignKey("Users", on_delete=models.CASCADE, related_name="notifications")
    isread = models.BooleanField(default=False)
    forPost = models.ForeignKey("Posts", on_delete=models.CASCADE, related_name="notifyPost")
    created = models.DateTimeField(auto_now_add=True)
    notification = models.CharField(max_length=1024)

    def __str__(self):
        return self.notification