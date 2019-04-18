from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.FileField(upload_to='profile_pics',blank=True)

    def __str__(self):
      return self.user.username


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=300)
    content = models.TextField()
    categories = models.CharField(max_length=300)
    icon = models.FileField()
    post_date = models.DateField('posted Date')

    def __str__(self):
        return self.title