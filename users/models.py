from django.db import models
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

# User = get_user_model()
class UserModel(AbstractUser):
    pass

class Profile(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png', blank=True)
    location = models.CharField(max_length=100, blank=True)
    update_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'profile'

