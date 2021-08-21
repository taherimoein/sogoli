from .models import User, UserManager, BeautyShop, Service, Post, Order
from django.contrib.auth import get_user_model
from django.contrib import admin

User = get_user_model()
# Main Section Title
admin.site.site_header = 'Sogoli'
# --------------------------------
# Order Admin Section
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('fk_user', 'fk_beautyshop', 'services', 'total_price', 'payment_status', 'order_date', 'reservation_date')
    search_fields = ['fk_user', 'fk_beautyshop', 'services']
    list_filter = ('publish', 'payment_status')
    ordering = ['id', 'order_date', 'reservation_date']
# Post Admin Section
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('fk_beautyshop', 'description', 'publish', 'create_date')
    search_fields = ['description']
    list_filter = ('publish',)
    ordering = ['id', 'create_date']
# Service Admin Section
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish', 'create_date')
    search_fields = ['title']
    list_filter = ('publish',)
    ordering = ['id', 'create_date']
# BeautyShop Admin Section
@admin.register(BeautyShop)
class BeautyShopAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'rate', 'publish', 'create_date')
    search_fields = ['title']
    list_filter = ('publish',)
    ordering = ['id', 'create_date']
# User Admin Section
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('mobile', 'first_name', 'last_name', 'superuser', 'staff', 'active', 'create_date')
    search_fields = ['mobile', 'first_name', 'last_name']
    list_filter = ('active',)
    ordering = ['id', 'create_date']
admin.site.register = (User, UserAdmin)
admin.site.register = (UserManager)