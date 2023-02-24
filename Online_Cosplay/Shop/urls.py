from django.urls import path
from . import views

urlpatterns = [
    path('shop/', views.shop, name='shop'),
    path('add_item/', views.add_item, name='additem'),
    path('add_to_cart/<int:id>', views.add_to_cart, name='addtocart'),
    path('cart/', views.cart, name='cart'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('remove/<int:id>', views.remove, name='remove'),
    path('payment_info/', views.payment_info, name='paymentinfo'),
    path('add_address/', views.add_address, name='addaddress'),
    path('select_address/', views.select_address, name='selectaddress'),
]