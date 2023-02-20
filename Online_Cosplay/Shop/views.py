from django.shortcuts import render, redirect
from .models import Item, Order, Cart
from .forms import NewItemForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def shop(request):
    return render(request, 'Shop/shop.html', {'items':Item.objects.all})

@login_required
def add_item(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
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
    conclusion = []
    for order in user_orders:
        conclusion.append({'name':order.item.name, 'price':f'{order.total_price:,.2f}'})
    total = f'{sum([order.total_price for order in user_orders]):,.2f}'
    return render(request, 'Shop/cart2.html', {'orders':user_orders, 'conclusion':conclusion, 'total':total})

@login_required
def dashboard(request):
    items = Item.objects.filter(user=request.user)
    return render(request, 'Shop/dashboard.html', {'items':items})

@login_required
def remove(request, id):
    item = Item.objects.get(id=id)
    if item.user == request.user:
        item.delete()
        messages.success(request, 'Remove item from cart successful.')
        return redirect('/dashboard')
    messages.error(request, "You don't have permission to remove this item.")
    return redirect('/dashboard')
        
@login_required
def payment(request):
    return render(request, 'Shop/payment.html')