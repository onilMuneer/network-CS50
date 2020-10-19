from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False)




class Post(models.Model):
    poster = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=1024 , blank=False, null=False)
    like = models.ManyToManyField("User", related_name='likes', symmetrical=False)


    def __str__(self):
        return f"{self.poster} : {self.pk}"
