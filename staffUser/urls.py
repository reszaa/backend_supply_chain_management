from django.urls import path
from . import views

urlpatterns = [
    # URL: http://127.0.0.1:8000/api/staff/register/
    path('register/', views.kelola_staff, name='register_staff'),
    path('login/', views.login_staff, name='login_staff'),
]

print("--- RUTE YANG TERDAFTAR DI STAFFUSER ---")
for url in urlpatterns:
    print(f"Path ditemukan: {url.pattern}")