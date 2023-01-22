from django.contrib import admin

from chat.models import PmMessages
from .models import Room, Message, Topic, User, Reglink
# Register your models here.

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Topic)
admin.site.register(User)
admin.site.register(PmMessages)
admin.site.register(Reglink)