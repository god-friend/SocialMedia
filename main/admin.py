from django.contrib import admin
from .forms import Users
from .models import Posts, Comments, Friends, Requests, Notifications, Likes
# Register your models here.


class UserAdmin(admin.ModelAdmin):    
    list_display = ["id", "username", "last_login", "created", "is_staff", "is_active", "is_superuser"]
    
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "__str__", "upload_date"]

class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "__str__", "created", "reply"]

class FriendsAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "friend", "created"]

class RequestAdmin(admin.ModelAdmin):
    list_display = ["id", "by", "to", "onDate"]

class NotificationsAdmin(admin.ModelAdmin):
    list_display = ["id", "to", "isread", "created", "notification", "forPost"]
    
class LikesAdmin(admin.ModelAdmin):
    list_display = ["id", "byUser", "likedPost"]

admin.site.register(Users, UserAdmin)
admin.site.register(Posts, PostAdmin)
admin.site.register(Comments, CommentAdmin)
admin.site.register(Friends, FriendsAdmin)
admin.site.register(Requests, RequestAdmin)
admin.site.register(Notifications, NotificationsAdmin)
admin.site.register(Likes, LikesAdmin)