
from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

