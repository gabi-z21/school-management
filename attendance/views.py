import json
from datetime import datetime
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import make_aware
from .models import Student, DailyAttendance, SMS

import sys
import serial
print(f"WORKER SHOULD USE THIS: {sys.executable}")
def home(request):
    return HttpResponse("working")


@property
def status(self):
    if self.check_in:
        return "Present"
    return "Absent"


@csrf_exempt
def receive_attendance(request):
    if request.method == "POST":
        data = json.loads(request.body)

        user_id = data.get("user_id")
        timestamp = data.get("timestamp")

        try:
            student = Student.objects.get(device_user_id=user_id)
            
            timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            timestamp = make_aware(timestamp)

            today = timestamp.date()
            record, created = DailyAttendance.objects.get_or_create(
                student=student,
                date=today
            )

            if record.check_in is None:
                record.check_in = timestamp
                record.save()
                return JsonResponse({"status": "check-in recorded"})
            
            elif record.check_out is None:
                record.check_out = timestamp
                record.save()
                return JsonResponse({"status": "check-out recorded"})
            
            else:
                return JsonResponse({"status": "already complete"})
            
        except Student.DoesNotExist:
            return JsonResponse({"error": "Student not found"}, status=404)
    return JsonResponse({"error": "invalid request"}, status=400)


def send_to_student(request, student_id): 
    student = Student.objects.get(id=student_id)
    message = request.GET.get("message")
    

    SMS.objects.create(
        student=Student,
        phone=student.phone,
        message=message

    )
    
    return JsonResponse({"status": "queued"})


def send_to_group(request):
    group = request.get('group')
    message = request.GET.get("message")

    students = Student.objects.filter(group=group)

    for s in students:
        SMS.objects.create(
            student=s,
            phone=s.add,
            message=message
        )

    return JsonResponse({"status": "group queued"})

