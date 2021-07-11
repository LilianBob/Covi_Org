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
def register(request):
    if request.method == 'GET':
        form  = RegisterForm()
        context = {'form': form}
        return render(request, 'signup.html', context)
    if request.method == 'POST':
        form  = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('email')
            messages.success(request, 'An account was succefully created for ' + user)
            return redirect('/login')
        messages.error(request, 'Errors occured while processing your request')
        context = {'form': form}
        return render(request, 'signup.html', context)
    return render(request, 'signup.html', {})