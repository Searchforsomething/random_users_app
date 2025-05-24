from django.db import models


class User(models.Model):
    gender = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=200)
    thumbnail = models.URLField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
