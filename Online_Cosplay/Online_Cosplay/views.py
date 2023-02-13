from django.shortcuts import render

def homepage(request):
    return render(request, 'Online_Cosplay/homepage.html')