
from urllib import request
import dotenv
import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Q
import razorpay

from .forms import RegistrationForm, LoginForm, ProfileUpdateForm, PasswordChangeForm
from .models import Book, Genre, CartItem, Order, ContactMessage
from django.shortcuts import get_object_or_404

# Load .env from the project root (same directory as manage.py)
_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
dotenv.load_dotenv(_env_path, override=True)

# Debug: confirm API keys loaded (remove in production)
print(f"[DEBUG] RAZORPAY_API_KEY loaded: {'Yes' if os.getenv('RAZORPAY_API_KEY') else 'No'}")
print(f"[DEBUG] RAZORPAY_API_SECRET loaded: {'Yes' if os.getenv('RAZORPAY_API_SECRET') else 'No'}")

# Create your views here.
def home(request):
    all_books = Book.objects.all()
    new_arrival_books = Book.objects.filter(newArrival=True).order_by('-published_date')
    bestseller_books = Book.objects.filter(bestseller=True).order_by('-rating')
    return render(
        request,
        'home.html',
        {
            'books': all_books,
            'new_arrival_books': new_arrival_books,
            'bestseller_books': bestseller_books,
        },
    )

def search_books(request):
    query = request.GET.get('q', '').strip()
    results = Book.objects.none()

    if query:
        results = (
            Book.objects.filter(
                Q(title__icontains=query)
                | Q(author__icontains=query)
                | Q(genre__name__icontains=query)
                | Q(isbn__icontains=query)
                | Q(description__icontains=query)
                | Q(publisher__icontains=query)
            )
            .distinct()
            .order_by('title')
        )

    return render(
        request,
        'search_results.html',
        {
            'query': query,
            'results': results,
            'results_count': results.count(),
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


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        if not name or not email or not message:
            messages.error(request, 'Please fill in all contact form fields.')
        else:
            ContactMessage.objects.create(name=name, email=email, message=message)
            messages.success(request, 'Thanks for contacting us! We will get back to you soon.')
            return redirect('contact')

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

    order_count = Order.objects.filter(user=user).count()
    cart_count = CartItem.objects.filter(user=user).count()

    return render(request, 'profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
        'order_count': order_count,
        'cart_count': cart_count,
        'orders': Order.objects.filter(user=user).order_by('-date_ordered'),
    })

def bookDetails(request):
    if request.POST:
        id=request.POST.get('id')
        book=Book.objects.get(id=id)
    return render(request, 'book_details.html', {'book': book})

def add_to_cart(request, id):
	if request.user.is_authenticated:
		product = Book.objects.get(id=id)
		cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
		cart_item.quantity += 1
		cart_item.save()
		return redirect('crtpage')
	else:
		return redirect('login')

def view_cart(request):
	if request.user.is_authenticated:
		cart_items = CartItem.objects.filter(user=request.user)
		total_price = sum(int(item.product.price) * item.quantity for item in cart_items)
		total_price=int(total_price)
		return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})
	else:
		return redirect('login')

@login_required
def update_cart(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Cart updated successfully.")
    return redirect('crtpage')  # 'cart' is the name of the cart view

@login_required
def delete_cart_item(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
    return redirect('crtpage')  # 'cartpage' is the name of the cart view


def books_by_genre(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    books = Book.objects.filter(genre=genre)

    return render(request, 'genre_books.html', {
        'genre': genre,
        'books': books
    })

@login_required
@csrf_exempt
def initiate_payment(request):
    if request.method == "POST":
        try:
            amount = int(request.POST["amount"]) * 100  # Amount in paise
            address = request.POST['address']

            api_key = os.getenv('RAZORPAY_API_KEY')
            api_secret = os.getenv('RAZORPAY_API_SECRET')

            print(f"[DEBUG] Payment attempt - Key: {api_key}, Secret: {'***' + api_secret[-4:] if api_secret else 'None'}")

            if not api_key or not api_secret:
                return JsonResponse({"error": "Payment gateway is not configured. Please contact support."}, status=500)

            client = razorpay.Client(auth=(api_key, api_secret))
            payment_data = {
                "amount": amount,
                "currency": "INR",
                "receipt": "order_receipt",
                "notes": {
                    "email": request.user.email,
                    "address": address,
                },
            }

            print(f"[DEBUG] Creating Razorpay order with data: {payment_data}")
            order = client.order.create(data=payment_data)
            print(f"[DEBUG] Razorpay order created successfully: {order['id']}")

            # Store address in session for use after payment success
            request.session['delivery_address'] = address

            response_data = {
                "id": order["id"],
                "amount": order["amount"],
                "currency": order["currency"],
                "key": api_key,
                "name": "Books Mart",
                "description": "Payment for Your Order",
                "image": "",
            }

            return JsonResponse(response_data)

        except razorpay.errors.BadRequestError as e:
            print(f"Razorpay BadRequestError: {e}")
            return JsonResponse({"error": f"Payment request error: {str(e)}"}, status=400)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Payment initiation error: {e}")
            return JsonResponse({"error": f"Payment failed: {str(e)}"}, status=500)

    return redirect('crtpage')


def payment_success(request):
    # Create orders and clear cart after successful payment
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        address = request.session.get('delivery_address', 'Not provided')
        if cart_items.exists():
            for cart in cart_items:
                Order.objects.get_or_create(
                    user=request.user,
                    product=cart.product,
                    quantity=cart.quantity,
                    payment_status='success',
                    address=address,
                )
            cart_items.delete()
            # Clear the session address
            if 'delivery_address' in request.session:
                del request.session['delivery_address']
    return render(request, "payment_success.html")

@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-date_ordered")
    return render(request, "my_orders.html", {"orders": orders})