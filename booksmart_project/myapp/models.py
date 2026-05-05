from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

# Create your models here.
# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None):
#         if not email:
#             raise ValueError("Please enter your email")
        
#         email=self.normalize_email(email)
#         user=self.model(email=email)
#         user.set_password(password)
#         user.save()

#     def create_superuser(self, email, password):
#         user=self.create_user(email, password)
#         user.is_staff=True
#         user.is_superuser=True
#         user.save(using=self._db)
#         return user

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Email is required')
        
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.is_active = True   # ✅ IMPORTANT
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError('Email is required')
        
        if not password:
            raise ValueError('Password is required')

        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=12)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Book(models.Model):
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    author = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    publisher = models.CharField(max_length=255)
    published_date = models.DateField()
    image = models.ImageField(upload_to='book_images/', null=True, blank=True,verbose_name="Book Image")
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, related_name='books')
    newArrival = models.BooleanField(default=True, verbose_name="New Arrival")
    bestseller = models.BooleanField(default=False, verbose_name="Bestseller")
    rating = models.DecimalField(max_digits=5, decimal_places=1, default=0.00)
    def __str__(self):
        return self.title
    

class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class CartItem(models.Model):
    product = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')  # prevent duplicates

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
    

class Order(models.Model):
    product = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    payment_status=models.CharField(max_length=255)
    payment_id=models.CharField(max_length=255)
    address=models.TextField()


class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} — {self.email}'