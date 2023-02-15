from django.urls import path
from . import views

urlpatterns = [
    path('shop/', views.shop, name='shop'),
    path('add_item/', views.add_item, name='additem'),
]