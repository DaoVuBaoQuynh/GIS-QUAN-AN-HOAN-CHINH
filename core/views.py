import math
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
from django.db.models import Count

from .models import Restaurant, Category, Reservation, Employee, DiningTable


# ====== Haversine distance (km) ======
def haversine_km(lat1, lng1, lat2, lng2):
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# ====== HOME MAP ======
def home_map(request):
    categories = Category.objects.all()
    center = {"lat": 12.67, "lng": 108.05, "zoom": 13}
    return render(request, "home_map.html", {
        "categories": categories,
        "center": center
    })


# ====== GEOJSON API ======
def restaurants_geojson(request):
    qs = Restaurant.objects.filter(is_active=True)

    q = request.GET.get("q")
    if q:
        qs = qs.filter(name__icontains=q)

    cat = request.GET.get("category")
    if cat and cat.isdigit():
        qs = qs.filter(category_id=int(cat))

    lat = request.GET.get("lat")
    lng = request.GET.get("lng")
    radius_km = request.GET.get("radius_km")

    if lat and lng and radius_km:
        try:
            u_lat = float(lat)
            u_lng = float(lng)
            r = float(radius_km)

            filtered = []
            for res in qs:
                d = haversine_km(u_lat, u_lng, res.latitude, res.longitude)
                if d <= r:
                    filtered.append((res, d))

            filtered.sort(key=lambda x: x[1])
            qs = [x[0] for x in filtered]
        except:
            pass

    features = []
    for res in qs:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [res.longitude, res.latitude]
            },
            "properties": {
                "id": res.id,
                "name": res.name,
                "address": res.address,
                "phone": res.phone,
                "category": res.category.name if res.category else None,
                "price_level": res.price_level,
            }
        })

    return JsonResponse({"type": "FeatureCollection", "features": features})


# ====== ĐẶT BÀN ======
def reserve(request):
    restaurants = Restaurant.objects.filter(is_active=True).order_by("name")

    if request.method == "POST":
        restaurant_id = request.POST.get("restaurant")
        customer_name = request.POST.get("customer_name", "").strip()
        customer_phone = request.POST.get("customer_phone", "").strip()
        guests = request.POST.get("guests")
        booking_time = request.POST.get("booking_time")
        note = request.POST.get("note", "").strip()

        if not all([restaurant_id, customer_name, customer_phone, guests, booking_time]):
            return render(request, "reserve.html", {
                "restaurants": restaurants,
                "error": "Vui lòng nhập đầy đủ thông tin!"
            })

        restaurant = get_object_or_404(Restaurant, id=restaurant_id)

        dt = timezone.make_aware(timezone.datetime.fromisoformat(booking_time))
        if dt <= timezone.now():
            return render(request, "reserve.html", {
                "restaurants": restaurants,
                "error": "Vui lòng chọn thời gian trong tương lai."
            })

        Reservation.objects.create(
            restaurant=restaurant,
            customer_name=customer_name,
            customer_phone=customer_phone,
            guests=int(guests),
            booking_time=dt,
            note=note,
            status="pending",
        )
        return redirect("reserve_success")

    return render(request, "reserve.html", {"restaurants": restaurants})


def reserve_success(request):
    return render(request, "reserve_success.html")


# ====== STAFF ======
def is_staff_user(user):
    return user.is_authenticated and Employee.objects.filter(user=user).exists()


@login_required
def staff_dashboard(request):
    if not is_staff_user(request.user):
        return HttpResponseForbidden("Bạn không phải nhân viên.")

    emp = Employee.objects.get(user=request.user)
    restaurant = emp.restaurant

    tables = DiningTable.objects.filter(restaurant=restaurant)
    reservations = Reservation.objects.filter(restaurant=restaurant).order_by("-created_at")[:50]

    return render(request, "staff_dashboard.html", {
        "restaurant": restaurant,
        "tables": tables,
        "reservations": reservations,
    })


@login_required
def update_table_status(request, table_id):
    if not is_staff_user(request.user):
        return HttpResponseForbidden("Không có quyền.")

    table = get_object_or_404(DiningTable, id=table_id)
    emp = Employee.objects.get(user=request.user)

    if table.restaurant_id != emp.restaurant_id:
        return HttpResponseForbidden("Không được sửa bàn quán khác.")

    if request.method == "POST":
        status = request.POST.get("status")
        if status in {"available", "reserved", "occupied", "cleaning"}:
            table.status = status
            table.save()

    return redirect("staff_dashboard")


# ====== THỐNG KÊ ======
def stats_by_category(request):
    data = (
        Restaurant.objects
        .values("category__name")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    return JsonResponse({
        "data": [
            {"category": d["category__name"] or "Chưa phân loại", "total": d["total"]}
            for d in data
        ]
    })
