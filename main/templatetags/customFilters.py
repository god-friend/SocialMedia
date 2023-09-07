from django import template
from main.models import Requests, Friends
from django.db.models import Q

register = template.Library()

@register.filter(name="transform")
def transform(x: list):
    new_L = []
    i = 0
    while(i < len(x)):
        new_L.append(x[i:i+3])
        i+=3
    # print(new_L)
    return new_L

@register.simple_tag
def setvar(x):
    return x

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
        if not are:
            return False
        return True
    except Friends.DoesNotExist:
        return False



@register.simple_tag
def call_method(obj, method, *args):
    func = getattr(obj, method)
    return func(*args)
    