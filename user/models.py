from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
  is_email_verified = models.BooleanField(default=False)
  email_verification_token = models.CharField(max_length=200 ,blank=True, null=True)

  def __str__(self):
    return self.first_name
  

class ContactUs(models.Model):
    first_name = models.CharField(max_length = 20)
    email = models.EmailField(null=False , unique=False)
    message = models.TextField(max_length = 500)

    def __str__(self):
        return self.message