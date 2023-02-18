from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
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
    return render(request, 'User/register2.html', {'register_form':form})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Welcome {username}!')
                return redirect('/')
        messages.error(request, 'Invalid username or password.')
    form = AuthenticationForm()
    return render(request, 'User/login2.html', {'login_form':form})

def logout_request(request):
    logout(request)
    messages.info(request, 'Logout Successfully.')
    return redirect('/')