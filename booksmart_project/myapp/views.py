
from urllib import request
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, LoginForm, ProfileUpdateForm, PasswordChangeForm
from .models import Book, Genre


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


@login_required(login_url='login')
def profile(request):
    user = request.user
    profile_form = ProfileUpdateForm(instance=user)
    password_form = PasswordChangeForm()

    if request.method == 'POST':
        form_type = request.POST.get('form_type', '')

        if form_type == 'profile_update':
            profile_form = ProfileUpdateForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile has been updated successfully!')
                return redirect('profile')
            else:
                for field, errors in profile_form.errors.items():
                    for error in errors:
                        messages.error(request, f'{error}')

        elif form_type == 'password_change':
            password_form = PasswordChangeForm(request.POST)
            if password_form.is_valid():
                current_password = password_form.cleaned_data['current_password']
                new_password = password_form.cleaned_data['new_password']

                if not user.check_password(current_password):
                    messages.error(request, 'Your current password is incorrect.')
                else:
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Your password has been changed successfully!')
                    return redirect('profile')
            else:
                for error in password_form.non_field_errors():
                    messages.error(request, error)

    return render(request, 'profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })

def bookDetails(request):
    if request.POST:
        id=request.POST.get('id')
        book=Book.objects.get(id=id)
    return render(request, 'book_details.html', {'book': book})