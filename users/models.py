from django.db import models
from django.contrib.auth.models import AbstractUser

''' 
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='userprofile', primary_key=True)
    profileImage = models.ImageField(upload_to='profileImages', blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
'''


class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profileImage = models.ImageField(upload_to='profileImages', blank=True, default='profileImages/default.jpg')

    def __str__(self):
        return self.username