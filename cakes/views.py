from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cake, Category, Review
from .forms import ReviewForm, CakeFilterForm


def home_view(request):
    featured_cakes = Cake.objects.filter(is_featured=True, is_active=True)[:6]
    categories = Category.objects.filter(is_active=True)[:8]
    latest_cakes = Cake.objects.filter(is_active=True)[:8]
    return render(request, 'cakes/home.html', {
        'featured_cakes': featured_cakes,
        'categories': categories,
        'latest_cakes': latest_cakes,
    })


def cake_list_view(request):
    cakes = Cake.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    form = CakeFilterForm(request.GET)

    # Search
    query = request.GET.get('q', '')
    if query:
        cakes = cakes.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(flavors__icontains=query) |
            Q(category__name__icontains=query)
        )

    # Filter by category
    category_slug = request.GET.get('category', '')
    if category_slug:
        cakes = cakes.filter(category__slug=category_slug)

    # Filter by price range
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price:
        cakes = cakes.filter(price__gte=min_price)
    if max_price:
        cakes = cakes.filter(price__lte=max_price)

    # Filter by availability
    availability = request.GET.get('availability', '')
    if availability:
        cakes = cakes.filter(availability=availability)

    # Sort
    sort = request.GET.get('sort', '-created_at')
    sort_options = {
        'price_asc': 'price',
        'price_desc': '-price',
        'name_asc': 'name',
        'name_desc': '-name',
        'newest': '-created_at',
        'oldest': 'created_at',
    }
    cakes = cakes.order_by(sort_options.get(sort, '-created_at'))

    # Pagination
    paginator = Paginator(cakes, 9)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    selected_category = None
    if category_slug:
        selected_category = Category.objects.filter(slug=category_slug).first()

    return render(request, 'cakes/cake_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'query': query,
        'selected_category': selected_category,
        'sort': sort,
        'min_price': min_price,
        'max_price': max_price,
        'availability': availability,
        'form': form,
    })


def cake_detail_view(request, slug):
    cake = get_object_or_404(Cake, slug=slug, is_active=True)
    reviews = cake.reviews.filter(is_approved=True)
    related_cakes = Cake.objects.filter(
        category=cake.category, is_active=True
    ).exclude(pk=cake.pk)[:4]
    user_review = None
    review_form = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
        if not user_review:
            review_form = ReviewForm()
    if request.method == 'POST' and request.user.is_authenticated:
        if not user_review:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.cake = cake
                review.user = request.user
                review.save()
                messages.success(request, 'Thank you for your review!')
                return redirect('cakes:detail', slug=slug)
    return render(request, 'cakes/cake_detail.html', {
        'cake': cake,
        'reviews': reviews,
        'related_cakes': related_cakes,
        'user_review': user_review,
        'review_form': review_form,
    })


def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    cakes = Cake.objects.filter(category=category, is_active=True)
    paginator = Paginator(cakes, 9)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'cakes/category.html', {
        'category': category,
        'page_obj': page_obj,
    })
