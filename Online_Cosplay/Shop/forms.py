from django.forms import ModelForm
from .models import Item, Address

class NewItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price', 'description', 'date', 'image']

class NewAddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'phone', 'address', 'zipcode']