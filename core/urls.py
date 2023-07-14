from django.urls import path, re_path
from . import views
from chat import views as viewss

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register/', views.register_user_preliminary, name='register'),
    # path(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
    path('logout/', views.logout_view, name='logout'),
    path('request-box/<str:pk>', views.request_box, name='request-box'),
    path('friends/<str:pkk>/e2AAS2accpt23487dhjbSS<str:pk>AD8U3Hisd3nO8',
         views.accept_friendship, name='accept'),
    path('friends/<str:pkk>/adsjnSI38DJjndas83DDNKjab<str:pk>dde3ubufeb',
         views.ignore_friendship, name='ignore'),
    path('7sn2njJHDAnd93983y4<str:pk>sabu62e3d9hidwdYWDG7G6t',
         views.retract_friendship, name='retract'),
    path('friends/<str:pkk>/adia7378VSJASjhsxdhD763Gjb<str:pk>dnsfi8GDg6sasvJHd2S5',
         views.delete_friendship, name='delete-fr'),
    path('d2983jfewubWEAJKE89<str:pk>LK8897hDSQ7Goiuad',
         views.send_friendship, name='bmf'),
    path('friends/<str:pk>/', views.friends_list, name='friends'),
    path('mfriends/<str:pk>/', views.friends_list_mobile, name='mfriends'),
    path('', views.home, name='home'),
    path('ajax/validate_username/',
         views.validate_username, name='validate-username'),
    path('room/<str:pk>/', views.room, name='room'),
    path('userprofile/<str:pk>/', views.user_profile, name='userprofile'),
    path('create-room/', views.create_room, name='create-room'),
    path('update-room/<str:pk>/', views.update_room, name='update-room'),
    path('update-user/', views.update_user, name='update-user'),
    path('activity-page/', views.activity_page, name='activity-page'),
    path('topics/', views.topics_page, name='topics'),
    path('delete-room/<str:pk>/', views.delete_room, name='delete-room'),
    path('delete-message/<str:pk>/', views.delete_message, name='delete-message'),
    path('delete-pm-message/<str:pk>',
         viewss.delete_pm_message, name='delete-pm-message'),
    path('loadmore/', views.load_more, name='loadmore'),
    re_path(
        r'\w+(\d|[a-z]|[A-Z]){6}(\d|[a-z]|[A-Z]){9}(\d){5}([A-Z]|[a-z]){5}[a-z]{3}(\d|[A-Z]|[a-z]){4}',
        views.register_user),
    path('status-checker/', views.status_checker, name="status_checker"),
    path('profile-status/<str:pk>', views.profile_status, name="profile_status"),
]
