# Generated by Django 3.1.1 on 2020-10-03 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yagakimi_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='webrtc_room_id',
            field=models.CharField(default='', max_length=50),
        ),
    ]
