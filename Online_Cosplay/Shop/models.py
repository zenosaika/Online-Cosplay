from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.
class Item(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    date = models.DateField(default=timezone.now)
    image = models.ImageField()

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.quantity} of {self.item} from {self.user}'
    
    @property
    def total_price(self):
        return self.item.price * self.quantity

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(Order)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}'