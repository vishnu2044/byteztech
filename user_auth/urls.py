from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    path('', views.login, name="login"),
    path('signup', views.signup, name="signup"),
    path('profile', views.profile, name="profile"),
    path('get-profile-details', views.get_profile_details, name="get-profile-details"),
    path('upload_page', views.upload_page, name="upload_page"),
    path('upload', views.upload_page, name='upload_page'),
    path('get_all_files', views.get_all_files, name='get_all_files'),

     path('logout', views.user_logout, name='logout'),

] 
