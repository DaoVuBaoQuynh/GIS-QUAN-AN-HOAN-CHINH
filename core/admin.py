from django.contrib import admin
from .models import Category, Restaurant, DiningTable, Reservation, Employee

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("id", "name",)

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price_level", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "address", "phone")

@admin.register(DiningTable)
class DiningTableAdmin(admin.ModelAdmin):
    list_display = ("id", "restaurant", "code", "capacity", "table_type", "status")
    list_filter = ("restaurant", "table_type", "status")
    search_fields = ("code",)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "customer_phone", "id", "restaurant", "booking_type", "guests", "status", "booking_time")
    list_filter = ("status", "restaurant", "booking_type")
    search_fields = ("customer_name", "customer_phone")

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "restaurant", "position", "status")
    list_filter = ("restaurant", "position", "status")
    search_fields = ("user__username", "user__email", "phone")
