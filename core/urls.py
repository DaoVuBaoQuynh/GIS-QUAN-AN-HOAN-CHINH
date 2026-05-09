from django.urls import path
from .views import home_map
from. import views

urlpatterns = [
    path('test-mail/', views.test_mail, name='test_mail'),

    path("restaurant/<int:restaurant_id>/review/delete/", views.delete_review, name="delete_review"),
    
    path("restaurant/<int:restaurant_id>/", views.restaurant_detail, name="restaurant_detail"),
    path("restaurant/<int:restaurant_id>/review/", views.add_review, name="add_review"),

    path("", views.landing_page, name="landing_page"),
    path("map/", views.home_map, name="home_map"),

    path("api/restaurants.geojson", views.restaurants_geojson, name="restaurants_geojson"),
    path("stats/category", views.stats_by_category),

    path("dat-ban/", views.reserve, name="reserve"),
    path("dat-ban/thanh-cong/", views.reserve_success, name="reserve_success"),

    path("login/staff/", views.staff_login_view, name="staff_login"),
    path("staff/", views.staff_dashboard, name="staff_dashboard"),
    path("staff/ban/<int:table_id>/cap-nhat/", views.update_table_status, name="update_table_status"),

    path("favorites/", views.my_favorites, name="my_favorites"),
    path("favorite/<int:restaurant_id>/toggle/", views.toggle_favorite, name="toggle_favorite"),

    path("dashboard/admin", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/admin/reservation/<int:reservation_id>/approve/", views.approve_reservation, name="approve_reservation"),
    path("dashboard/admin/reservation/<int:reservation_id>/reject/", views.reject_reservation, name="reject_reservation"),
    
    path("profile/", views.user_profile, name="user_profile"),

    path('map/add-restaurant/', views.add_restaurant_from_map, name='add_restaurant_from_map'),
    path('map/delete-restaurant/<int:id>/', views.delete_restaurant, name='delete_restaurant'),

    path("dashboard/hang-hoa/", views.hang_hoa, name="hang_hoa"),
    path("dashboard/hang-hoa/delete/<int:product_id>/", views.delete_product, name="delete_product"),
    
    path("update-price/", views.update_price, name="update_price"),

    path("update-stock/<int:product_id>/", views.update_stock, name="update_stock"),

    path("dashboard/hang-hoa/export/", views.export_products, name="export_products"),

    path("dashboard/admin/export-revenue/", views.export_revenue_excel, name="export_revenue_excel"),

    path("dashboard/nhan-vien/", views.nhan_vien, name="nhan_vien"),
    path("dashboard/nhan-vien/delete/<int:employee_id>/", views.delete_employee, name="delete_employee"),

    path("dashboard/nhan-vien/check-in/<int:employee_id>/", views.check_in_employee, name="check_in_employee"),
    path("dashboard/nhan-vien/check-out/<int:employee_id>/", views.check_out_employee, name="check_out_employee"),

    path("dashboard/nhan-vien/export-salary/", views.export_salary_excel, name="export_salary_excel"),

    path("dashboard/nhan-vien/cap-nhat-hieu-suat/", views.update_employee_performance, name="update_employee_performance"),

    path("dashboard/phong-ban/", views.phong_ban, name="phong_ban"),

    path("dashboard/phong-ban/save/", views.save_table, name="save_table"),
    path("dashboard/phong-ban/delete/<int:table_id>/", views.delete_table, name="delete_table"),
    path("dashboard/phong-ban/status/<int:table_id>/<str:status>/", views.change_table_status, name="change_table_status"),
    
    path("dashboard/phong-ban/duyet/<int:reservation_id>/", views.approve_booking_from_table, name="approve_booking_from_table"),

    path("dashboard/bao-cao/", views.bao_cao, name="bao_cao"),
    path("dashboard/bao-cao/export-excel/", views.export_bao_cao_excel, name="export_bao_cao_excel"),

]
