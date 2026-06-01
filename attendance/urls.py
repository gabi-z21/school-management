from django.urls import path
from .views import receive_attendance, send_to_student, send_to_group

urlpatterns = [
    path('api/attendance/', receive_attendance),
    path('api/attendance/', send_to_student),
    path('api/attendance', send_to_group
         )

]
