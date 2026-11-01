from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Cake(models.Model):
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('out_of_stock', 'Out of Stock'),
        ('pre_order', 'Pre-Order'),
    ]

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='cakes')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    weight = models.CharField(max_length=50, help_text='e.g., 500g, 1kg')
    serves = models.PositiveIntegerField(default=6, help_text='Number of people it serves')
    flavors = models.CharField(max_length=300, help_text='Comma-separated flavors, e.g., Chocolate, Vanilla')
    ingredients = models.TextField(blank=True)
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='available')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    thumbnail = models.ImageField(upload_to='cakes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_effective_price(self):
        return self.discount_price if self.discount_price else self.price

    def get_discount_percentage(self):
        if self.discount_price:
            return round((1 - self.discount_price / self.price) * 100)
        return 0

    def get_average_rating(self):
        reviews = self.reviews.filter(is_approved=True)
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0

    def get_review_count(self):
        return self.reviews.filter(is_approved=True).count()

    def get_flavors_list(self):
        return [f.strip() for f in self.flavors.split(',')]


class CakeImage(models.Model):
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='cakes/gallery/')
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.cake.name} - Image {self.order}"


class Review(models.Model):
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    comment = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cake', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.cake.name} ({self.rating}/5)"
