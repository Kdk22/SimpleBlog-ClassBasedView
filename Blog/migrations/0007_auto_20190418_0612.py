# Generated by Django 2.2 on 2019-04-18 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0006_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofileinfo',
            name='user',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='UserProfileInfo',
        ),
    ]
