from django.db import models


class GirlsLove(models.Model):
    follower_name = models.CharField(max_length=50)
    followee_name = models.CharField(max_length=50)
