# NextTask/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'NextTask/home.html')