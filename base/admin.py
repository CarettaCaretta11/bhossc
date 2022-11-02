from django.contrib import admin

from chat.models import pm_messages
from .models import Photos, Room, Message, Topic, User
# Register your models here.

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Topic)
admin.site.register(User)
admin.site.register(pm_messages)
admin.site.register(Photos)
