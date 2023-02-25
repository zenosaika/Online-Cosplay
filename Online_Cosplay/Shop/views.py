from django.shortcuts import render, redirect
from .models import Item, Order, Cart, ShippingInformation
from .forms import NewItemForm, NewAddressForm
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
def payment_info(request):
    if not ShippingInformation.objects.filter(user=request.user):
        shipping_info = ShippingInformation(user=request.user)
        shipping_info.save()
    try:
        user_orders = Cart.objects.get(user=request.user).items.all()
        conclusion = []
        for order in user_orders:
            conclusion.append({'name':order.item.name, 'price':f'{order.total_price:,.2f}'})
        total = f'{sum([order.total_price for order in user_orders]):,.2f}'
        user_addresses = ShippingInformation.objects.get(user=request.user).address.all()
        selected_address = user_addresses.filter(selected=True)
        return render(request, 'Shop/payment_info.html', {'conclusion':conclusion, 'total':total, 'addresses':user_addresses, 'selected_address':selected_address})
    except:
        return redirect('/cart')
    
@login_required
def add_address(request):
    if request.method == 'POST':
        address = NewAddressForm(request.POST)
        if address.is_valid():
            address = address.save(commit=False)
            address.user = request.user
            address.selected = True
            address.save()

            shipping_info = ShippingInformation.objects.filter(user=request.user)
            if shipping_info:
                selected_address = shipping_info[0].address.filter(selected=True)
                for addr in selected_address:
                    addr.selected = False
                    addr.save()
                shipping_info[0].address.add(address)
                shipping_info[0].save()
            else:
                new_shipping_info = ShippingInformation(user=request.user)
                new_shipping_info.address.add(address)
                new_shipping_info.save()

            messages.success(request, 'Add new address successful.')
            return redirect('/payment_info')
        else:
            messages.error(request, 'Invalid information.')
            return redirect('/payment_info')
    else:
        address = NewAddressForm()
        return render(request, 'Shop/add_address.html', {'new_address_form':address})

def select_address(request):
    shipping_info = ShippingInformation.objects.filter(user=request.user)
    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address')
        if selected_address_id:
            selected_address = shipping_info[0].address.filter(selected=True)
            for addr in selected_address:
                addr.selected = False
                addr.save()
            new_selected_address = shipping_info[0].address.get(id=selected_address_id)
            new_selected_address.selected = True
            new_selected_address.save()
            messages.success(request, 'Change address successful.')
            return redirect('/payment_info')
        else:
            messages.error(request, 'Please select an address before submit.')
            return redirect('/select_address')
    addresses = []
    if shipping_info:
        addresses = shipping_info[0].address.all()
    return render(request, 'Shop/select_address.html', {'addresses':addresses})