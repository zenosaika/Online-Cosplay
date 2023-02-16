from django.shortcuts import render, redirect
from .models import Item, Order, Cart
from .forms import NewItemForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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

@login_required
def add_to_cart(request, id):
    item = Item.objects.filter(id=id)
    if item:
        order = Order.objects.filter(user=request.user, item=item[0], ordered=False)
        if order:
            order[0].quantity += 1
            order[0].save()
        else:
            new_order = Order(user=request.user, item=item[0], quantity=1, ordered=False)
            new_order.save()
            cart = Cart.objects.filter(user=request.user, ordered=False)
            if cart:
                cart[0].items.add(new_order)
                cart[0].save()
            else:
                new_cart = Cart(user=request.user, ordered=False)
                new_cart.save()
    else:
        messages.error(request, "Sorry, we don't have this item.")
        return redirect('/shop')
    messages.success(request, 'Add item to cart successful.')
    return redirect('/cart')

@login_required
def cart(request):
    if not Cart.objects.filter(user=request.user):
        cart = Cart(user=request.user, ordered=False)
        cart.save()
    user_orders = Cart.objects.get(user=request.user).items.all()
    return render(request, 'Shop/cart.html', {'orders':user_orders})
        