from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    skills = models.CharField(max_length=300)

    def __str__(self):
        return self.user.username
