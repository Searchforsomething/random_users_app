from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class User(models.Model):
    gender = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=200)  # Объединённое поле "город, страна"
    thumbnail = models.URLField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"slug": self.slug})
