from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class List(models.Model):
    name = models.TextField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="list")
    description = models.TextField(max_length=400, default="")
    public = models.BooleanField(default=True)
    everyday_uncheck = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_reset = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{"public" if self.public == True else "private"}: {self.name}"

class Item(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="item")
    checked =  models.BooleanField(default=False)
    content = models.TextField(max_length=100)

    def __str__(self):
        return f"Item in {self.list.name}: {self.content}"