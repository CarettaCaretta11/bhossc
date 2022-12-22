from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    path('rooms/', views.get_rooms),
    path('room/<str:pk>/', views.get_room),
    path('rooms/create/', views.create_room),
    path('room/<str:pk>/update/', views.RoomRetrieveUpdateAPIView.as_view()),
    path('room/<str:pk>/delete/', views.RoomDeleteAPIView.as_view()),
    path('users/', views.get_users, name='users'),
    path('user/<str:pk>', views.get_user, name='user'),
    path('users/create/', views.create_user),
    path('user/<str:pk>/update/',
         views.UserRetrieveUpdateAPIView.as_view(), name='update-user'),
    path('user/<str:pk>/delete/',
         views.UserDeleteAPIView.as_view(), name='delete-user'),
    path('messages/', views.get_messages),
    path('message/<str:pk>', views.get_message),
    path('messages/create/', views.create_message),
    path('message/<str:pk>/delete/', views.MessageDeleteAPIView.as_view()),
]
