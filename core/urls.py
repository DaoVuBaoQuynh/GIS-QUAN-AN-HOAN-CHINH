from django.urls import path
from .views import home_map
from. import views

urlpatterns = [
    path("", views.home_map, name="home"),
    path("api/restaurants.geojson", views.restaurants_geojson, name="restaurants_geojson"),
    path("stats/category", views.stats_by_category),

    path("dat-ban/", views.reserve, name="reserve"),
    path("dat-ban/thanh-cong/", views.reserve_success, name="reserve_success"),

    path("staff/", views.staff_dashboard, name="staff_dashboard"),
    path("staff/ban/<int:table_id>/cap-nhat/", views.update_table_status, name="update_table_status"),
]
