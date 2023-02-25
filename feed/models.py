from django.db import models

import uuid

from users.models import UserModel


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    number_of_likes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return '%s %s' %(self.user.first_name, self.user.last_name)