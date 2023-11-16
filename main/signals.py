from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save

from .models import Posts, Requests, Comments, Notifications, Likes

from .extras import delete_post_pics

from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

import json

layer = get_channel_layer()

@receiver(post_save, sender=Posts)
def notify_friend_new_post(sender, instance, **kwargs):
    if not instance.post_text:
        return
    
    try:
        obj = sender.objects.get(id=instance.id)
    except:
        data = {
            "gotNewPost": "You got new Posts"
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
    group = "user_{0}".format(instance.to.id)
    from_user = instance.by.firstname + " " + instance.by.lastname
    count = Requests.objects.filter(to=instance.to).count()
    data = {
        "count": count,
        "gotRequest": "You got a new Friend Request from " + from_user
    }
    async_to_sync(layer.group_send)(group, {
        "type": "send.update",
        "text": json.dumps(data)
    })


@receiver(post_delete, sender=Requests)
def notify_user_del_request(sender, instance, **kwargs):
    group = "user_{0}".format(instance.to.id)
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
    
    group = "user_{0}".format(toUser.id)
    nData = {
        "gotComment": noti.notification
    }
    async_to_sync(layer.group_send)(group, {
        "type": "send.update",
        "text": json.dumps(nData)
    })


@receiver(post_save, sender=Notifications)
def update_count(sender, instance, **kwargs):
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


@receiver(post_save, sender=Likes)
def notify_user_like(sender, instance, **kwargs):
    postByUser = instance.likedPost.by
    likedByUser = instance.byUser
    
    if postByUser != likedByUser:
        data = {
            "to": postByUser,
            "forPost": instance.likedPost,
            "notification": likedByUser.get_fullname() + " Liked Your post.",
        }
        
        noti = Notifications.objects.create(**data)
    
    
        group = "user_{0}".format(postByUser.id)
        data = {
            "gotLike": noti.notification,
        }
        async_to_sync(layer.group_send)(group, {
            "type": "send.update",
            "text": json.dumps(data)
        })