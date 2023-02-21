from django.contrib import admin
from .models import Item, Order, Cart, Address, ShippingInformation

# Register your models here.
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Address)
admin.site.register(ShippingInformation)