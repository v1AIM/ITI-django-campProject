from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone

from .managers import CustomUserManager

# Create your models here.


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=254, unique=True)
    mobile = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(r"^\d{11}$", message="Mobile Number Must be 11 digits")
        ],
        help_text="Required. Your 11-digit mobile number.",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    object = CustomUserManager()

    def __str__(self):
        return self.email


class Project(models.Model):
    title = models.CharField(max_length=100)
    details = models.TextField(max_length=1000)
    total_target = models.PositiveIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount_donated = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.start_time > self.end_time:
            raise ValueError("Start time must be before end time")
        super().save(*args, **kwargs)
