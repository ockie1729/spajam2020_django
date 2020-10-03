from django.db import models

# Create your models here.


class User(models.Model):
    uuid = models.CharField(max_length=50)
    twitter_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)


class Room(models.Model):
    webrtc_room_id = models.CharField(max_length=50)
    uuid = models.CharField(max_length=50)


class Text(models.Model):
    text = models.TextField()
    uuid = models.CharField(max_length=50)
    watson_response = models.TextField()
    tokenized_text = models.TextField()
    created_at = models.DateTimeField()
