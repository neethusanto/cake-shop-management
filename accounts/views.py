from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import CustomerRegistrationForm, LoginForm, ProfileUpdateForm
from .models import User
from orders.models import Order


def register_view(request):
    if request.user.is_authenticated:
        return redirect('cakes:home')
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}! Your account has been created.')
            return redirect('cakes:home')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('cakes:home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'cakes:home')
            return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('cakes:home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, 'accounts/profile.html', {'form': form, 'orders': orders})


@login_required
def dashboard_view(request):
    if not request.user.is_admin_user() and not request.user.is_staff_user():
        messages.error(request, 'You do not have permission to access the dashboard.')
        return redirect('cakes:home')
    from cakes.models import Cake
    from orders.models import Order
    context = {
        'total_cakes': Cake.objects.count(),
        'total_orders': Order.objects.count(),
        'total_users': User.objects.count(),
        'recent_orders': Order.objects.order_by('-created_at')[:10],
        'pending_orders': Order.objects.filter(status='pending').count(),
    }
    return render(request, 'accounts/dashboard.html', context)
