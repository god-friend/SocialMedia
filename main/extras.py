import os
from django.conf import settings
from datetime import datetime

MEDIA_DIR = settings.MEDIA_ROOT


def check_and_create_dir(path, dirname):
    if os.path.exists(path+'/'+dirname):
        return 
    os.mkdir(path+'/'+dirname)


def upload_profile_pic(instance, file):
    check_and_create_dir(MEDIA_DIR, 'dp')
    fileExt = file.split(".")[1]
    now = datetime.now()
    filename = now.strftime("%Y%m%d-%H%M%S.%f") + "." + fileExt
    
    return 'dp/user_{0}/{1}'.format(instance.id, filename)


def getAllPics(path):
    # print(MEDIA_DIR)
    return os.listdir(MEDIA_DIR+path)


def upload_post_pics(file, user_id, post_id):
    check_and_create_dir(MEDIA_DIR, "posts")
    check_and_create_dir(MEDIA_DIR+"/posts" , "user_{0}".format(user_id))
    check_and_create_dir(MEDIA_DIR+"/posts/user_{0}".format(user_id), "post_{0}".format(post_id))
    fileExt = file.name.split(".")[1]
    now = datetime.now()
    fileName = now.strftime("%Y%m%d-%H%M%S.%f") + "." + fileExt
    file_path = MEDIA_DIR + "/posts/user_{0}/post_{1}/".format(user_id, post_id) 
    url = "media/posts/user_{0}/post_{1}/{2}".format(user_id, post_id, fileName)
    with open(file_path+fileName, "wb+") as dest:
        for chunk in file.chunks():
            dest.write(chunk)
    
    dest.close()
    
    return (file_path, url)


def delete_post_pics(instance):
    if not instance.pics_path:
        return
    pics = os.listdir(instance.pics_path)
    for p in pics:
        os.remove(instance.pics_path+p)
    os.rmdir(instance.pics_path)


# Need to delete Dir if empty
def delPic(picLocation):
    filePath = MEDIA_DIR + "/" + picLocation
    exists = os.path.exists(filePath)
    if exists:
        os.remove(filePath)
        
