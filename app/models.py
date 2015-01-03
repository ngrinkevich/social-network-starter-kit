# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.core.urlresolvers import reverse

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from social.apps.django_app.default.models import UserSocialAuth

class UserManager(BaseUserManager):

    @classmethod
    def normalize_email(cls, email):
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email

    def make_random_password(self, length=10, 
                             allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                           'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                           '23456789'):
        return get_random_string(length, allowed_chars)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


    def create_user(self, email, gender=0, password=None, request=None, username=None, display_name='New User', *args, **kwargs):
    
        if not email:
            msg = 'Users must have an email address'
            raise ValueError(msg)
        if gender is None:
            msg = 'Users must provide Gender'
            raise ValueError(msg)
    
        user = self.model(email=self.normalize_email(email), gender=0, username=username, display_name=display_name)
        user.is_active=True
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, gender=0, password=None, display_name='Super User'):
        user = self.create_user(email, gender=gender, password=password, display_name=display_name)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

GENDER_CHOICES = [
    (0,   'male'),
    (1,   'female'),
]

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(verbose_name='Email Address', max_length=255, unique=True, db_index=True)
    USERNAME_FIELD = 'email'
    
    username = models.CharField(max_length=255, blank=True, null=True)
    
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    gender = models.IntegerField(choices=GENDER_CHOICES)
    display_name = models.CharField(max_length=255, blank=True, null=True) 
    
    about = models.TextField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    avatar_thumb = ImageSpecField(source='avatar', processors=[ResizeToFill(150, 150)], format='JPEG', options={'quality': 90})
    avatar_ext = models.CharField(max_length=255, blank=True, null=True)

    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    
    objects = UserManager()
    
    def get_full_name(self):
        return "%s" % (self.display_name)
    
    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.display_name
    
    def get_facebook_avatar(self, width, height):
        try:
            connections = UserSocialAuth.objects.all().filter(user = self, provider = 'facebook')
            if connections[0].uid:
                return 'https://graph.facebook.com/%s/picture?type=large&width=%s&height=%s'%(connections[0].uid,width, height)
        except:
            return

    def get_avatar(self):
        avatar = self.get_facebook_avatar(300,300)
        if avatar:
            return avatar
        elif self.avatar:
            return self.avatar.url
        elif self.avatar_ext:
            return self.avatar_ext
        else:    
            return 'http://placehold.it/300x300.png'
    
    def get_avatar_thumb(self):
        avatar = self.get_facebook_avatar(140,140)
        if avatar:
            return avatar
        elif self.avatar:
            return self.avatar_thumb.url
        elif self.avatar_ext:
            return self.avatar_ext
        else:    
            return 'http://placehold.it/140x140.png'

    def get_absolute_url(self):
        return reverse('profile', args=[str(self.id)])
    
