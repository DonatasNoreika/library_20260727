from django.db import models

# Create your models here.

class Genre(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"