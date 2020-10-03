from django.urls import path

from . import views

urlpatterns = [
    path('user/create', views.user_create, name='user_create'),
    path('line/push', views.push_room_id_to_line, name='push_room_id_to_line')
]
