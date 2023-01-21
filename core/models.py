import datetime
# import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import utc
from django.conf import settings
from cloudinary.models import CloudinaryField


class Photos(models.Model):
    photo = CloudinaryField('image')


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)
    # models.DateTimeField(auto_now_add=True) would make it uneditable
    # The field is only automatically updated when calling Model.save().
    # The field 'DateField.auto_now' isn’t updated when making updates to other fields in other ways
    # such as QuerySet.update(),though you can specify a custom value for the field in an update like that.
    last_time_visited = models.DateTimeField(auto_now=True)
    # avatar = models.ImageField(null=True, default='avatar.svg')
    # avatar = models.ForeignKey(Photos, null=True, default='avatar.svg')
    avatar = CloudinaryField(
        'image', default='https://res.cloudinary.com/dn3laf4bh/image/upload/v1647623057/avatar_iu9mmi.svg')
    pending_invs = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='pending_invs1', blank=True)
    # Two instances of User model ~ so we change one to friends1
    # note: related_name specifies the name of the reverse relation, so we make it different than the direct one
    friends = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='friends1', blank=True)
    USERNAME_FIELD = 'email'
    # A list of the field names that will be prompted
    # for when creating a user via the createsuperuser management command
    REQUIRED_FIELDS = ['username']
    # confirmed = models.BooleanField(editable=True, default=False)

    def __str__(self):
        return self.username

    def get_time_diff(self):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        timediff = now - self.last_time_visited
        return timediff.total_seconds()

    # @staticmethod
    # def salt(self):
    #     return str(random.random())[2:]


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
        # (optional) “-” prefix indicates descending order.
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
