from django.db import models
from django.utils import timezone

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    date = models.DateField(default=timezone.now)
    image = models.ImageField()

    def __str__(self):
        return self.name