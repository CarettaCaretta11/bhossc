from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from core.models import Room, User, Message

# The default ModelSerializer uses primary keys for relationships


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class UserSerializer(ModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    update = serializers.SerializerMethodField()
    delete = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'name',
            'email',
            'bio',
            'absolute_url',
            'update',
            'delete',
        ]

    def get_absolute_url(self, obj):
        return reverse('user', args={obj.id, })

    def get_update(self, obj):
        return reverse('update-user', args={obj.id, })

    def get_delete(self, obj):
        return reverse('delete-user', args={obj.id, })


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
