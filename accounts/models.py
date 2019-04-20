from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from sms.utils import send_transactional_sms

class UserManager(BaseUserManager):
    def create_user(self, phone, full_name=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not phone:
            raise ValueError("Users must have a phone number")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            phone = phone,
            full_name=full_name
        )
        user_obj.set_password(password) # change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, phone,full_name=None, password=None):
        user = self.create_user(
                phone,
                full_name=full_name,
                password=password,
                is_staff=True
        )
        return user

    def create_superuser(self, phone, full_name=None, password=None):
        user = self.create_user(
                phone,
                full_name=full_name,
                password=password,
                is_staff=True,
                is_admin=True
        )
        return user


class User(AbstractBaseUser):
    phone       = models.CharField(max_length=10, unique=True)
    email       = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    full_name   = models.CharField(max_length=255, blank=True, null=True)
    is_active   = models.BooleanField(default=True) # can login 
    staff       = models.BooleanField(default=False) # staff user non superuser
    admin       = models.BooleanField(default=False) # superuser 
    timestamp   = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone' 
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone
    
    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.phone

    def get_short_name(self):
        if self.full_name:
            return self.full_name
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

def post_save_user_create_reciever(sender, instance, created, *args, **kwargs):
    if created:
        send_transactional_sms({instance.phone}, "Welcome to Pustakalay.")
#         send message to user.

post_save.connect(post_save_user_create_reciever, sender=User)
