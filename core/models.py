from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("restaurant", "user")

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name} ({self.rating} sao)"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True, null=True)

    latitude = models.FloatField()
    longitude = models.FloatField()

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    price_level = models.PositiveSmallIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    image_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Employee(models.Model):
    POSITION_CHOICES = [
        ("manager", "Quản lý"),
        ("cashier", "Thu ngân"),
        ("waiter", "Phục vụ"),
        ("kitchen", "Bếp"),
        ("shipper", "Giao hàng"),
    ]

    STATUS_CHOICES = [
        ("active", "Đang làm"),
        ("inactive", "Nghỉ làm"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    position = models.CharField(max_length=30, choices=POSITION_CHOICES, default="waiter")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    avatar = models.ImageField(upload_to="employees/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    bonus = models.IntegerField(default=0)
    penalty = models.IntegerField(default=0)  # tiền phạt

    def __str__(self):
        return self.user.username


class DiningTable(models.Model):
    TABLE_TYPE_CHOICES = [
        ("normal", "Bàn thường"),
        ("vip", "Bàn VIP"),
    ]

    STATUS_CHOICES = [
        ("available", "Còn trống"),
        ("reserved", "Đã đặt"),
        ("occupied", "Đang phục vụ"),
        ("cleaning", "Đang dọn"),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    capacity = models.IntegerField(default=2)
    table_type = models.CharField(max_length=10, choices=TABLE_TYPE_CHOICES, default="normal")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")

    class Meta:
        unique_together = ("restaurant", "code")
        ordering = ["restaurant", "code"]

    def __str__(self):
        return f"{self.restaurant.name} - {self.code}"


class Reservation(models.Model):
    TABLE_BOOKING_TYPE = [
        ("normal", "Bàn thường"),
        ("vip", "Bàn VIP"),
    ]

    STATUS_CHOICES = [
        ("pending", "Chờ xác nhận"),
        ("confirmed", "Đã xác nhận"),
        ("cancelled", "Đã hủy"),
    ]

    status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default="pending"
)


    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    guests = models.IntegerField()
    booking_time = models.DateTimeField()
    note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    booking_type = models.CharField(max_length=10, choices=TABLE_BOOKING_TYPE, default="normal")
    created_at = models.DateTimeField(auto_now_add=True)
class Meta:
        ordering = ["-created_at"]

def __str__(self):
        return f"{self.customer_name} - {self.restaurant.name}"


class FavoriteRestaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite_restaurants")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "restaurant")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} ♥ {self.restaurant.name}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='default.png')

class Product(models.Model):
    FOOD_TYPES = [
        ("mon_an", "Món ăn"),
        ("do_uong", "Đồ uống"),
        ("combo", "Combo/Buffet"),
        ("dich_vu", "Dịch vụ"),
        ("che_bien", "Hàng chế biến"),
    ]

    STATUS_CHOICES = [
        ("active", "Đang kinh doanh"),
        ("inactive", "Ngừng kinh doanh"),
        ("out_of_stock", "Hết hàng"),
    ]

    code = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=200)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    food_type = models.CharField(max_length=30, choices=FOOD_TYPES, default="mon_an")
    price = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    min_stock = models.PositiveIntegerField(default=0)
    max_stock = models.PositiveIntegerField(default=999)

    image = models.ImageField(upload_to="products/", blank=True, null=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="active")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class WorkShift(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.name


class Attendance(models.Model):
    STATUS_CHOICES = [
        ("on_time", "Đúng giờ"),
        ("late", "Đi muộn"),
        ("absent", "Vắng"),
        ("left_early", "Về sớm"),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    shift = models.ForeignKey(WorkShift, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="on_time")
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.employee.user.username} - {self.date}"


class EmployeePerformance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    total_work_days = models.IntegerField(default=0)
    late_days = models.IntegerField(default=0)
    absent_days = models.IntegerField(default=0)
    score = models.IntegerField(default=100)

    def __str__(self):
        return f"{self.employee.user.username} - {self.month}/{self.year}"

class RestaurantTable(models.Model):

    STATUS_CHOICES = [
        ("available", "Trống"),
        ("reserved", "Đã đặt"),
        ("occupied", "Đang dùng"),
        ("cleaning", "Đang dọn"),
    ]

    TYPE_CHOICES = [
        ("normal", "Bàn thường"),
        ("vip", "VIP"),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    code = models.CharField(max_length=20)

    table_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    capacity = models.IntegerField(default=4)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="available"
    )

    # DRAG POSITION
    pos_x = models.IntegerField(default=50)
    pos_y = models.IntegerField(default=50)

    def __str__(self):
        return self.code

class TableReservation(models.Model):

    STATUS_CHOICES = [
        ("pending", "Chờ duyệt"),
        ("confirmed", "Đã duyệt"),
        ("late", "Tới trễ"),
        ("cancelled", "Huỷ bàn"),
        ("completed", "Hoàn thành"),
    ]

    table = models.ForeignKey(
        RestaurantTable,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    customer_name = models.CharField(max_length=100)

    customer_phone = models.CharField(max_length=20)

    guests = models.IntegerField(default=2)

    booking_time = models.DateTimeField()

    end_time = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    note = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name
    
