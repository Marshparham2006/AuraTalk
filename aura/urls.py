from django.urls import path
from . import views

app_name = 'aura'

urlpatterns = [
    path('', views.home, name='home'),
    path('choose-username/', views.choose_username, name='choose_username'),
    path('chat/', views.chat_rooms, name='chat_rooms'),
    path('create-room/', views.create_room, name='create_room'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('google123456789.html', views.google_verification, name='google_verification'),
    path('sitemap.xml', views.sitemap, name='sitemap'),
   path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots_txt'),
]
