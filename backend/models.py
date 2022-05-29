from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ProfileInfo(models.Model):

    CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    profile_image = models.ImageField(
        upload_to='profile/image', null=True, blank=True)
    about = models.TextField()
    address = models.CharField(max_length=128)
    sex = models.CharField(max_length=5, choices=CHOICES, default='F')

    def __str__(self):
        return self.name


class SocialAccount(models.Model):
    user = models.ForeignKey(
        User, related_name='social_handles', on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    handle = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.handle
