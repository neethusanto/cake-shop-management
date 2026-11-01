from django.contrib import admin
from .models import Category, Cake, CakeImage, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_filter = ['is_active']


class CakeImageInline(admin.TabularInline):
    model = CakeImage
    extra = 3


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'discount_price', 'availability', 'is_featured', 'is_active']
    list_filter = ['category', 'availability', 'is_featured', 'is_active']
    search_fields = ['name', 'description', 'flavors']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_featured', 'is_active', 'availability']
    inlines = [CakeImageInline]
    fieldsets = (
        ('Basic Info', {'fields': ('category', 'name', 'slug', 'description', 'thumbnail')}),
        ('Pricing', {'fields': ('price', 'discount_price')}),
        ('Details', {'fields': ('weight', 'serves', 'flavors', 'ingredients')}),
        ('Status', {'fields': ('availability', 'is_featured', 'is_active')}),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'cake', 'rating', 'title', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating']
    search_fields = ['user__username', 'cake__name', 'title']
    list_editable = ['is_approved']
