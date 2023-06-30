from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to="profile_pictures", null=True)
