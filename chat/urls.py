from . import views
from django.urls import path

urlpatterns = [
    # path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='chat'),
]