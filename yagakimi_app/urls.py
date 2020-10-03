from django.urls import path

from . import views

urlpatterns = [
    path('user/create', views.user_create, name='user_create'),
    path('topic/register_text', views.topic_register_text,
         name='topic_register_text'),
]
