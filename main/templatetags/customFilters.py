from django import template
from main.models import Requests, Friends
from django.db.models import Q

register = template.Library()

@register.filter(name="transform")
def transform(x: list, n:int):
    # print(n)
    new_L = []
    i = 0
    while(i < len(x)):
        new_L.append(x[i:i+n])
        i+=n
    # print(new_L)
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
    # print(from_user, to_user)
    try:
        req = Requests.objects.get(by=from_user, to=to_user)
        # print(req)
        return True
    except Requests.DoesNotExist:
        return False
    
@register.simple_tag
def areFriends(cUser, fUser):
    try:
        f = (Q(user=cUser) & Q(friend=fUser)) | (Q(user=fUser) & Q(friend=cUser))
        are = Friends.objects.filter(f)
        # print(are)
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