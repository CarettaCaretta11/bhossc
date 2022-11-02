from django.db import models
import datetime
from django.utils.timezone import utc
from django.db.models.deletion import CASCADE
from base.models import User

# time1 = datetime.datetime.now()
# additional_hours = datetime.timedelta(hours=4)
# post_time = time1 + additional_hours

# def set_creation_time():
#     additional_hours = datetime.timedelta(hours=4)
#     post_time = datetime.datetime.now() + additional_hours

class pm_messages(models.Model):
    body = models.TextField()
    sender = models.CharField(max_length=255, null=True)
    room = models.CharField(max_length=255, null=True)
    created = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.body[0:10]
        
    class Meta:
        ordering = ['created']

    def get_time_diffr(self):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        timediff = now - self.created
        return timediff.total_seconds()