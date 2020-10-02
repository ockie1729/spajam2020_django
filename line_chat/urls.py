from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # no1にpushメッセージを送る
    path('webhook/', views.webhook, name='webhook')

]
