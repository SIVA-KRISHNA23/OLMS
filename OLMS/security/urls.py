from django.urls import path
from . import views

urlpatterns = [
    path('scan/', views.qr_code_scanner, name='qr_code_scanner'),
    path('user-details/<str:email>/', views.user_details, name='user_details'),
    path('scanned_today/', views.scanned_today, name='scanned_today'),
]

