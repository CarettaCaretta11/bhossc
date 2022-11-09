from cgitb import lookup
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.status import HTTP_201_CREATED
from rest_framework.decorators import api_view
from base.models import Room, User, Message
from .serializers import RoomSerializer, UserSerializer, MessageSerializer
from api import serializers

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api/',
        'GET /api/rooms',
        'GET /api/room/:id',
        'POST /api/rooms/create',
        'PUT /api/room/:id/update',
        'DELETE /api/room/:id/delete',
        'GET /api/users',
        'GET /api/user/:id',
        'POST /api/users/create',
        'PUT /api/user/:id/update',
        'DELETE /api/user/:id/delete',
        'GET /api/messages/',
        'GET /api/message/:id',
        'POST /api/messages/create',
        'DELETE /api/message/:id/delete',
    ]
    return Response(routes) # safe => can use lists etc.

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room)
    return Response(serializer.data)

@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getUser(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
def getMessages(request):
    messages = Message.objects.all()
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getMessage(request, pk):
    message = Message.objects.get(id=pk)
    serializer = MessageSerializer(message)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def createRoom(request):
    if request.method == 'POST':
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = {
                'msg': 'Room object has been created.'
            }
            return Response(res, status=HTTP_201_CREATED)
        else:
            return Response({
                'msg': 'An error occured.'
            })
    else:
        return Response({
            'msg': 'Write down the attributes to create a Room object.'
        })

@api_view(['GET', 'POST'])
def createUser(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = {
                'msg': 'User object has been created.'
            }
            return Response(res, status=HTTP_201_CREATED)
        else:
            return Response({
                'msg': 'An error occured.'
            })
    else:
        return Response({
            'msg': 'Write down the attributes to create a User object.'
        })

@api_view(['GET', 'POST'])
def createMessage(request):
    if request.method == 'POST':
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = {
                'msg': 'Message object has been created.'
            }
            return Response(res, status=HTTP_201_CREATED)
        else:
            return Response({
                'msg': 'An error occured.'
            })
    else:
        return Response({
            'msg': 'Write down the attributes to create a Message object.'
        })

class RoomRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    lookup_field = "pk"
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    lookup_field = "pk"
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RoomDeleteAPIView(generics.DestroyAPIView):
    lookup_field = "pk"
    queryset = Room.objects.all()

class UserDeleteAPIView(generics.DestroyAPIView):
    lookup_field = "pk"
    queryset = User.objects.all()

class MessageDeleteAPIView(generics.DestroyAPIView):
    lookup_field = "pk"
    queryset = Message.objects.all()