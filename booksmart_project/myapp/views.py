
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import RegistrationForm, LoginForm
from .models import Book


# Create your views here.
def home(request):
    all_books = Book.objects.all()
    featured_books = Book.objects.order_by('-published_date')[:8]
    return render(
        request,
        'home.html',
        {
            'books': all_books,
            'featured_books': featured_books,
        },
    )

def register(request):
    form=RegistrationForm(request.POST or None)
    if request.method=="POST":
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Account created successfully! Please log in.')
                return redirect('login')
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
                messages.success(request, f'Welcome back, {user.first_name or user.email}! You are now logged in.')
                return redirect('home-page')
            else:
                messages.error(request, 'Invalid email or password. Please try again.')
        else:
            messages.error(request, 'Please enter a valid email and password.')
    return render(request, 'login.html', {'form':form})

def logoutUser(request):
    logout(request)
    return redirect('login')


def contact(request):
    # if request.method == "POST":
    #     name = request.POST.get("name", "").strip()
    #     email = request.POST.get("email", "").strip()
    #     message = request.POST.get("message", "").strip()

    #     if not name or not email or not message:
    #         messages.error(request, 'Please fill in all contact form fields.')
    #     else:
    #         messages.success(request, 'Thanks for contacting us. We will get back to you soon!')
    #         return redirect('contact')

    return render(request, 'contact.html')