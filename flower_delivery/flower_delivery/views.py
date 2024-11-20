from django.shortcuts import render

def home(request):
    return render(request, 'flower_delivery/home.html')
