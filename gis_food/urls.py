"""
URL configuration for gis_food project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from core import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("core.urls")),
    #login#
    path("login/admin/", views.admin_login_view, name="admin_login"),
    path("login/user/", views.user_login_view, name="user_login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path('logout/', LogoutView.as_view(next_page='user_login'), name='logout'),
    path('staff/login', views.staff_login_view, name='staff_login'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/hang-hoa/', views.hang_hoa, name='hang_hoa'),
    path('map/add-restaurant/', views.add_restaurant_from_map, name='add_restaurant_from_map'),
    path('map/delete-restaurant/<int:id>/', views.delete_restaurant, name='delete_restaurant'),
    #dashboard riêng#
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
    path("profile/", views.profile, name="profile"),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

