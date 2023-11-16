from django import template
from main.models import Requests, Friends, Likes
from django.db.models import Q

register = template.Library()

@register.filter(name="transform")
def transform(x: list, n:int):
    new_L = []
    i = 0
    while(i < len(x)):
        new_L.append(x[i:i+n])
        i+=n
    return new_L

@register.simple_tag
def setvar(x):
    return x

@register.simple_tag
def createString(*args):
    string = ""
    for x in args:
        string += str(x)
    return string

@register.simple_tag
def isRequested(from_user, to_user):
    try:
        req = Requests.objects.get(by=from_user, to=to_user)
        return True
    except Requests.DoesNotExist:
        return False
    
@register.simple_tag
def isLiked(user, post):
    count = Likes.objects.filter(byUser=user, likedPost=post).count()
    
    if count > 0:
        return True
    
    return False

@register.simple_tag
def areFriends(cUser, fUser):
    try:
        f = (Q(user=cUser) & Q(friend=fUser)) | (Q(user=fUser) & Q(friend=cUser))
        are = Friends.objects.filter(f)
        if not are:
            return False
        return True
    except Friends.DoesNotExist:
        return False



@register.simple_tag
def call_method(obj, method, *args):
    func = getattr(obj, method)
    return func(*args)
    
    
@register.simple_tag
def isDefaultImg(imgPath):
    
    imgPath = str(imgPath)
    
    lastSlash = imgPath.rfind("/")
    imgName = imgPath[lastSlash+1:]
    
    if imgName == "default-user.png":
        return True
    
    return False