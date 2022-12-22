from django.db import models
import datetime
from django.utils.timezone import utc


class PmMessages(models.Model):
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
