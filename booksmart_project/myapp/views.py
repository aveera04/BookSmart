
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import RegistrationForm, LoginForm


# Create your views here.
def home(request):
    return render(request, 'home.html')

def register(request):
    form=RegistrationForm(request.POST or None)
    if request.method=="POST":
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Registration is successfull')
            except Exception as e:
                messages.error(request, e)
    return render(request, 'register.html', {'form':form})

def loginUser(request):
    form=LoginForm()
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home-page')
    return render(request, 'login.html', {'form':form})

def logoutUser(request):
    logout(request)
    return redirect('login')