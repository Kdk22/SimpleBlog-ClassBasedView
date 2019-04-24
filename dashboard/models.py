from django.db import models

# Create your models here.

# from Blog.models import  Post, UserProfileInfo, User

# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete= models.CASCADE)
#     posts = models.ForeignKey(Post, on_delete = models.CASCADE)
#     comment_text = models.CharField(max_length=500)
#     comment_date = models.DateField()
#
#     def __str__(self):
#         return self.comment_text+ '-' + str(self.user)