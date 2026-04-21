from django.urls import path
from .views import receive_attendance, home

urlpatterns = [
    path('', home),
    path('api/attendance/', receive_attendance),
]
