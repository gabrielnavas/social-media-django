from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

class User(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True,
    )

    USERNAME_FIELD = 'email'
    
    class Meta:
        db_table = 'user'
    
    def __str__(self) -> str:
        return self.email

        

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100)

    class Meta:
        db_table = 'profile'

    def __str__(self) -> str:
        return self.user.get_username()

