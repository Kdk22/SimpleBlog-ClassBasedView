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

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    posts = models.ForeignKey(Post, on_delete = models.CASCADE)
    comment_text = models.CharField(max_length=500)
    comment_date = models.DateField()

    def __str__(self):
        return self.comment_text+ '-' + str(self.user)