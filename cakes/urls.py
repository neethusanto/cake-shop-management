from django.urls import path
from . import views

app_name = 'cakes'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('cakes/', views.cake_list_view, name='list'),
    path('cakes/<slug:slug>/', views.cake_detail_view, name='detail'),
    path('category/<slug:slug>/', views.category_view, name='category'),
]
