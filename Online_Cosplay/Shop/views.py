from django.shortcuts import render, redirect
from .models import Item
from .forms import NewItemForm
from django.contrib import messages

# Create your views here.
def shop(request):
    return render(request, 'Shop/shop.html', {'items':Item.objects.all})

def add_item(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Add item successful.')
            return redirect('/shop')
        messages.error(request, 'Invalid information.')
    form = NewItemForm()
    return render(request, 'Shop/add_item.html', {'add_item_form':form})