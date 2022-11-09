from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('rooms/', views.getRooms),
    path('room/<str:pk>/', views.getRoom),
    path('rooms/create/', views.createRoom),
    path('room/<str:pk>/update/', views.RoomRetrieveUpdateAPIView.as_view()),
    path('room/<str:pk>/delete/', views.RoomDeleteAPIView.as_view()),
    path('users/', views.getUsers, name='users'),
    path('user/<str:pk>', views.getUser, name='user'),
    path('users/create/', views.createUser),
    path('user/<str:pk>/update/', views.UserRetrieveUpdateAPIView.as_view(), name='update-user'),
    path('user/<str:pk>/delete/', views.UserDeleteAPIView.as_view(), name='delete-user'),
    path('messages/', views.getMessages),
    path('message/<str:pk>', views.getMessage),
    path('messages/create/', views.createMessage),
    path('message/<str:pk>/delete/', views.MessageDeleteAPIView.as_view()),
]