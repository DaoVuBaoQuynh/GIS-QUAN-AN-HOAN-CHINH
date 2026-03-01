from django.contrib import admin
from .models import Category, Restaurant, DiningTable, Reservation, Employee

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "phone", "category", "price_level", "is_active")
    list_filter = ("category", "is_active", "price_level")
    search_fields = ("name", "address")

@admin.register(DiningTable)
class DiningTableAdmin(admin.ModelAdmin):
    list_display = ("restaurant", "code", "seats", "status")
    list_filter = ("restaurant", "status")
    search_fields = ("code",)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "customer_phone", "restaurant", "booking_time", "guests", "status", "created_at")
    list_filter = ("status", "restaurant")
    search_fields = ("customer_name", "customer_phone")

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("user", "restaurant", "role")
    list_filter = ("restaurant", "role")
