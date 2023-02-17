from django.forms import ModelForm
from .models import Item

class NewItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price', 'description', 'date', 'image']