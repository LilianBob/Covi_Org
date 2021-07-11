from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm
from django.contrib import messages

# Create your views here.
def index(request):
    context={
        'health_condition': 'Covid-19',
        'required_action': 'self screen and report your vaccine status'
    }
    return render(request, 'home.html', context)