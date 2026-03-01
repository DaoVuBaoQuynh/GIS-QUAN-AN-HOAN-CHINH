from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)

    # tọa độ (lat/lng)
    latitude = models.FloatField()
    longitude = models.FloatField()

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    price_level = models.PositiveSmallIntegerField(default=1)  # 1-5
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="employees")
    role = models.CharField(max_length=50, default="staff")  # staff/manager

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name}"


class DiningTable(models.Model):
    STATUS = [
        ("available", "Trống"),
        ("reserved", "Đã đặt"),
        ("occupied", "Đang phục vụ"),
        ("cleaning", "Đang dọn"),
    ]
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="tables")
    code = models.CharField(max_length=30)     # T1, T2
    seats = models.PositiveIntegerField(default=4)
    status = models.CharField(max_length=20, choices=STATUS, default="available")

    class Meta:
        unique_together = ("restaurant", "code")

    def __str__(self):
        return f"{self.restaurant.name} - {self.code}"


class Reservation(models.Model):
    STATUS = [
        ("pending", "Chờ duyệt"),
        ("confirmed", "Đã xác nhận"),
        ("cancelled", "Đã huỷ"),
        ("done", "Hoàn tất"),
    ]
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="reservations")
    table = models.ForeignKey(DiningTable, on_delete=models.SET_NULL, null=True, blank=True)

    customer_name = models.CharField(max_length=120)
    customer_phone = models.CharField(max_length=30)
    guests = models.PositiveIntegerField(default=2)
    booking_time = models.DateTimeField()
    note = models.CharField(max_length=300, blank=True)

    status = models.CharField(max_length=20, choices=STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.restaurant.name} ({self.status})"
