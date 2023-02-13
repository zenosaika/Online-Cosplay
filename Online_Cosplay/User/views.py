from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib import messages

# Create your views here.
def register_request(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration Successful!')
            return redirect('/')
        messages.error(request, 'Invalid Information.')
    form = RegisterForm()
    return render(request, 'User/register.html', {'register_form':form})