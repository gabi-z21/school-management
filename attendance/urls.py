from django.urls import path
from .views import receive_attendance, home, send_to_student, send_to_group

urlpatterns = [
    path('', home),
    path('api/attendance/', receive_attendance),
    path('api/attendance/', send_to_student),
    path('api/attendance', send_to_group
         )

]
