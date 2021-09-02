from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('screen', views.screen),
    path('screened', views.screened),
    path('vaccine_reporting', views.vaccine_reporting),
    path('vreported', views.vreported),
    path('file_upload/<int:user_id>', views.file_upload),
    path('profile/<int:user_id>', views.profile),
    path('delete_profile/<int:user_id>', views.delete_profile),
    path('edit/<int:user_id>', views.profile_update),
    path('feed', views.feed),
    path('newsPost', views.newsPost),
    path('add_newsPost', views.add_newsPost),
    path('news_postContent/<int:newsPost_id>', views.news_content),
    path('like/<int:newsPost_id>', views.add_like),
    path('comment/<int:newsPost_id>', views.add_comment),
    path('comments/<int:newsPost_id>', views.comments),
    path('delete_post/<int:newsPost_id>', views.delete_post),
]