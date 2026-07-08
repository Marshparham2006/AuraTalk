from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from aura import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('choose-username/', views.choose_username, name='choose_username'),
    path('chat/', views.chat_rooms, name='chat_rooms'),
    path('chat/<int:room_id>/', views.chat_room, name='chat_room'),
    path('profile/', views.profile, name='profile'),
    path('create-room/', views.create_room, name='create_room'),
    path('update-profile/', views.update_profile, name='update_profile'),  
    path('update-avatar/', views.update_avatar, name='update_avatar'),
    path('sitemap.xml', views.sitemap, name='sitemap'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    # دوست‌یابی
    path('friend-list/', views.friend_list, name='friend_list'),
    path('send-friend-request/', views.send_friend_request, name='send_friend_request'),
    path('accept-friend-request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject-friend-request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),

# چت خصوصی
    path('private-chat/<int:room_id>/', views.private_chat_room, name='private_chat_room'),
    path('get-private-rooms/', views.get_private_rooms, name='get_private_rooms'),
    path('get-private-messages/<int:room_id>/', views.get_private_messages, name='get_private_messages'),
    path('get-or-create-private-room/', views.get_or_create_private_room, name='get_or_create_private_room'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)