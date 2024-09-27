# NextTask/views.py
from django.shortcuts import render
from django.utils.translation import gettext as _


def home(request):
    context = {
        'Freelancer' : _('Freelancer')
    }
    return render(request, 'NextTask/home.html', context)