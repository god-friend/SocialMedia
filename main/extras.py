import os
from django.conf import settings

MEDIA_DIR = settings.MEDIA_ROOT


def check_and_create_dir(path, dirname):
    if os.path.exists(path+'/'+dirname):
        return 
    os.mkdir(path+'/'+dirname)


def upload_profile_pic(instance, file):
    check_and_create_dir(MEDIA_DIR, 'dp')

    return 'dp/user_{0}/{1}'.format(instance.id, file)


def get_all_profile_pics(path):
    return os.listdir(MEDIA_DIR+path)


def upload_post_pics(file, user_id, post_id):
    check_and_create_dir(MEDIA_DIR, "posts")
    check_and_create_dir(MEDIA_DIR+"/posts" , "user_{0}".format(user_id))
    check_and_create_dir(MEDIA_DIR+"/posts/user_{0}".format(user_id), "post_{0}".format(post_id))

    file_path = MEDIA_DIR + "/posts/user_{0}/post_{1}/".format(user_id, post_id) 
    url = "media/posts/user_{0}/post_{1}/{2}".format(user_id, post_id, file.name)
    with open(file_path+file.name, "wb+") as dest:
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

def delProfilePic(picLoc):
    filePath = MEDIA_DIR+"/"+picLoc
    exists = os.path.exists(filePath)
    if exists:
        os.remove(filePath)


def html_alert(message):
    html = '''<div class="position-absolute">
    <div class="alert alert-success alert-dismissible" role="alert">{0}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    </div>'''.format(message)
    return html