from unicodedata import name
from django.urls import path, re_path
from . import views
from chat import views as viewss

urlpatterns = [
    path('login/', views.loginpage, name='login'),
    path('register/', views.register_user_preliminary, name='register'),
    # path(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
    path('logout/', views.logout_view, name='logout'),
    path('request-box/<str:pk>', views.request_box, name='request-box'),
    path('friends/<str:pkk>/e2AAS2accpt23487dhjbSS<str:pk>AD8U3Hisd3nO8', views.accept_friendship, name='accept'),
    path('friends/<str:pkk>/adsjnSI38DJjndas83DDNKjab<str:pk>dde3ubufeb', views.ignore_friendship, name='ignore'),
    path('7sn2njJHDAnd93983y4<str:pk>sabu62e3d9hidwdYWDG7G6t', views.retract_friendship, name='retract'),
    path('friends/<str:pkk>/adia7378VSJASjhsxdhD763Gjb<str:pk>dnsfi8GDg6sasvJHd2S5', views.delete_friendship, name='delete-fr'),
    path('d2983jfewubWEAJKE89<str:pk>LK8897hDSQ7Goiuad', views.send_friendship, name='bmf'),
    path('friends/<str:pk>/', views.friends_list, name='friends'),
    path('mfriends/<str:pk>/', views.friends_list_mobile, name='mfriends'),
    # path('request-box/<str:pk>/confirm', views.sndc, name='sndc'),
    # path('request-box/<str:pk>/activate/AGiauTDF2D27FT8Vaq76dfHDFu63dfdshs783dtSV63f', views.confirm_a, name='confirma'),
    path('', views.home, name='home'),
    # path('woozie/', views.AjaxHandlerView.as_view()),
    path('ajax/validate_username/', views.validate_username, name='validate-username'),
    # path('ajax/validate_password/', views.validate_password, name='validate-password'),
    # path('d2983jfewubWEAJKE89LK8897hDSQ7Goiuad/ajax/friendship_alert', views.alert_friendship, name='sfa'),
    path('room/<str:pk>/', views.room, name='room'),
    path('userprofile/<str:pk>/', views.userprofile, name='userprofile'),
    path('create-room/', views.createroom, name='create-room'),
    path('update-room/<str:pk>/', views.updateroom, name='update-room'),
    path('update-user/', views.updateuser, name='update-user'),
    path('activity-page/', views.ActivityPage, name='activity-page'),
    path('topics/', views.topicsPage, name='topics'),
    path('delete-room/<str:pk>/', views.deleteroom, name='delete-room'),
    path('delete-message/<str:pk>/', views.deletemessage, name='delete-message'),
    path('delete-pm-message/<str:pk>', viewss.deletepmmessage, name='delete-pm-message'),
    path('loadmore/', views.loadmore, name='loadmore'),
    # path('register/', views.register_user_preliminary, name='register1'),
    re_path(r'\w+(\d|[a-z]|[A-Z]){6}(\d|[a-z]|[A-Z]){9}(\d){5}([A-Z]|[a-z]){5}[a-z]{3}(\d|[A-Z]|[a-z]){4}', views.register_user),
    path('status-checker/', views.status_checker, name="status_checker"),
    path('profile-status/<str:pk>', views.profile_status, name="profile_status"),
]