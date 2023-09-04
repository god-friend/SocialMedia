from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _

class UsersManager(BaseUserManager):

    def create_user(self, username, password=None, **kwargs):
        if not username:
            raise ValueError(_("User must have an username"))
        
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, username, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError(_("SuperUser must be staff"))
        if kwargs.get('is_superuser') is not True:
            raise ValueError(_("SuperUser must be a superuser"))
        
        return self.create_user(username, password, **kwargs)
    

