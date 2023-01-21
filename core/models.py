import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import utc
from django.conf import settings
from cloudinary.models import CloudinaryField


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)
    last_time_visited = models.DateTimeField(auto_now=True)
    avatar = CloudinaryField(
        'image', default='https://res.cloudinary.com/dn3laf4bh/image/upload/v1647623057/avatar_iu9mmi.svg')
    pending_invs = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='pending_invs1', blank=True)
    friends = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='friends1', blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def get_time_diff(self):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        timediff = now - self.last_time_visited
        return timediff.total_seconds()


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    thumbnail = CloudinaryField('image', blank=True, null=True, default='')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

    def get_time_diffr(self):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        timediff = now - self.created
        return timediff.total_seconds()


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:10]

    class Meta:
        ordering = ['-updated', '-created']

    def get_time_diffr(self):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        timediff = now - self.created
        return timediff.total_seconds()
