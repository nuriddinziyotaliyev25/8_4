from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Customer, Order, Category, Food

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['pk', 'full_name', 'email', 'phone', 'address']
    list_display_links = ['pk', 'full_name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'slug']
    list_display_links = ['pk', 'title']
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'slug', 'category', 'description', 'price', 'available', 'show_image']
    list_display_links = ['pk', 'title']
    def show_image(self, obj):
        return mark_safe(f'<img src="{obj.get_image()}" alt="No image" width="60px" height="60px">')
    show_image.short_description = 'Rasm'

    prepopulated_fields = {"slug": ("title",)}


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'customer', 'show_items',  'status', 'date']
    list_display_links = ['pk', 'customer']
    def show_items(self, obj):
        items = obj.items.all()
        return [item.title for item in items]
    show_items.short_description = "Taomlar"