from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save

from .models import Posts, Requests, Comments, Notifications

from .extras import delete_post_pics, html_alert

from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

import json


layer = get_channel_layer()



@receiver(post_save, sender=Posts)
def notify_friend_new_post(sender, instance, **kwargs):
    if not instance.post_text:
        return
    
    data = {
        "html": html_alert("You got new Posts")
    }

    friends = instance.by.friends()
    for friend in friends:
        group = "user_{0}".format(friend[0])
        async_to_sync(layer.group_send)(group, {
            "type": "send.update",
            "text": json.dumps(data)
        })


@receiver(post_delete, sender=Posts)
def delete_files(sender, instance, **kwargs):
    delete_post_pics(instance)



@receiver(post_save, sender=Requests)
def notify_user_request(sender, instance, **kwargs):
    # layer = get_channel_layer()
    group = "user_{0}".format(instance.to.id)
    # print(group)
    from_user = instance.by.firstname + " " + instance.by.lastname
    count = Requests.objects.filter(to=instance.to).count()
    data = {
        "count": count,
        "html": html_alert("You got a new Friend Request from "+from_user)
    }
    async_to_sync(layer.group_send)(group, {
        "type": "send.update",
        "text": json.dumps(data)
    })

@receiver(post_delete, sender=Requests)
def notify_user_del_request(sender, instance, **kwargs):
    # layer = get_channel_layer()
    group = "user_{0}".format(instance.to.id)
    # print(group)
    count = Requests.objects.filter(to=instance.to).count()
    data = {
        "count": count,
    }
    async_to_sync(layer.group_send)(group, {
        "type": "send.update",
        "text": json.dumps(data)
    })

@receiver(post_save, sender=Comments)
def notify_user_comment(sender, instance, **kwargs):
    toUser = instance.forPost.by
    byUser = instance.user
    data = {
        "to": toUser,
        "forPost": instance.forPost,
    }

    if toUser != byUser:
        if instance.isParent():
            data["notification"] = byUser.get_fullname() + " Commented on Your Post." 
        else:
            toUser = instance.reply.user
            data["notification"] = byUser.get_fullname() + " Replied to Your Comment."
            data["to"] = toUser
            if toUser == instance.user:
                return
    else:
        if not instance.isParent():
            toUser = instance.reply.user
            data["notification"] = byUser.get_fullname() + " Replied to Your Comment."
            data["to"] = toUser
            if toUser == instance.user:
                return
        else:
            return

    noti = Notifications.objects.create(**data)
    
    count = toUser.notify_count()
    group = "user_{0}".format(toUser.id)
    nData = {
        "ncount": count,
        "html": html_alert("You got a new Notification.")
    }
    async_to_sync(layer.group_send)(group, {
        "type": "send.update",
        "text": json.dumps(nData)
    })

@receiver(post_save, sender=Notifications)
def update_count(sender, instance, **kwargs):
    if instance.isread == True:
        toUser = instance.to
        count = toUser.notify_count()
        group = "user_{0}".format(toUser.id)
        nData = {
            "ncount": count,
        }
        async_to_sync(layer.group_send)(group, {
            "type": "send.update",
            "text": json.dumps(nData)
        })
