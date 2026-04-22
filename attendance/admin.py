from django.contrib import admin
from .models import Student, DailyAttendance, SMS

# Register your models here.

admin.site.register(Student)
admin.site.register(DailyAttendance)
admin.site.register(SMS)
