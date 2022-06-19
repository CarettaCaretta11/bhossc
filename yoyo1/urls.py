from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.static import serve 

urlpatterns = [
    path('adminkamransqrt-1/', admin.site.urls),
    path('chat/', include('chat.urls')),
    path('api/', include('api.urls')),
    path('', include('base.urls')),
    path('password-reset', auth_views.PasswordResetView.as_view(template_name='base/password_reset.html'), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='base/password_reset_confirm.html'), name='password_reset_confirm'), # uidb64 = user id in base 64, token: Password recovery token to check that the password is valid.
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='base/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-complete', auth_views.PasswordResetCompleteView.as_view(template_name='base/password_reset_complete.html'), name='password_reset_complete'),
    # url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    # url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# If DEBUG is set to True (in your settings module), then your 404 view will never be used, and your URLconf will be displayed instead, with some debug information.
# handler404 = "yoyo1.views.page_not_found_view"
