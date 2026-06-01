import json
import requests
import xml.etree.ElementTree as ET
import time
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import make_aware
from .models import Student, SMS
from .sms_service import SMSService
from .sync import process_attendance

sms_gateway = SMSService()


@csrf_exempt
def receive_attendance(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)

        user_id = str(data.get("user_id", "")).strip()
        timestamp_str = data.get("timestamp")

        if not user_id or not timestamp_str:
            return JsonResponse({"error": "Missing user_id or timestamp"}, status=400)

        student = Student.objects.filter(device_user_id=user_id).first()
        if not student:
            return JsonResponse({"error": "Student not found"}, status=404)

        try:
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            timestamp = make_aware(timestamp)
        except ValueError:
            return JsonResponse({"error": "Bad timestamp format"}, status=400)

        process_attendance(user_id, timestamp)

        return JsonResponse({"status": "success"})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON payload"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=500)


def send_to_student(request, student_id): 
    student = get_object_or_404(Student, id=student_id)
    message = request.GET.get("message")

    if not message:
        return JsonResponse({"error": "Message parameter is required"}, status=400)
    
    sms_log = SMS.objects.create(
        student=student,
        phone=student.phone_number,
        message=message,
        batch_name="Individual",
    )
    success = sms_gateway.send_sms(student.phone_number, message)
    
    # 3. Update status based on hardware response
    if success:
        sms_log.status = 'sent'
    else:
        sms_log.status = 'failed'
    sms_log.save()

    return JsonResponse({"status": "sent", "sms_id": sms_log.id})


def send_to_group(request):
    group = request.GET.get('group')
    message = request.GET.get("message")

    if not group or not message:
        return JsonResponse({"error": "Missing group or message parameters"}, status=400)

    students = Student.objects.filter(group=group)

    for s in students:
        SMS.objects.create(
            student=s,
            phone=s.phone_number,
            message=message,
        )
        sms_gateway.send_sms(s.phone_number, message)

    return JsonResponse({"status": "group queued"})


class SMSService:
    def __init__(self, base_url='http://192.168.8.1'):
        self.base_url = base_url
        time.sleep(2)

    def _get_tokens(self):
        """Fetches session and verification tokens from HiLink API."""
        try:
            response = requests.get(
                f"{self.base_url}/api/webserver/token", timeout=5
            )
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                # Modern HiLink firmware returns both cookies and tokens
                ses = root.find('SesInfo')
                tok = root.find('TokInfo')
                session_info = ses.text if ses is not None else None
                tok_info = tok.text if tok is not None else None
                return session_info, tok_info
        except Exception as e:
            print(f"Error connecting to Huawei Modem: {e}")
        return None, None

    def send_sms(self, phone, message):
        """Sends an SMS payload via HTTP POST to the modem."""
        session_info, tok_info = self._get_tokens()
        if not session_info or not tok_info:
            print("Failed to authenticate with modem. SMS not sent.")
            return False

        url = f"{self.base_url}/api/sms/send-sms"
        
        # Format required XML payload for Huawei modems
        payload = f"""<?xml version='1.0' encoding='UTF-8'?>
        <request>
            <Index>-1</Index>
            <Phones><Phone>{phone}</Phone></Phones>
            <Sca></Sca>
            <Content>{message}</Content>
            <Length>{len(message)}</Length>
            <Reserved>1</Reserved>
            <Date>-1</Date>
        </request>"""

        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "__RequestVerificationToken": tok_info,
            "Cookie": session_info,
            "Content-Type": "application/xml"
        }

        try:
            res = requests.post(url, data=payload, headers=headers, timeout=5)
            if "OK" in res.text:
                print(f"SMS successfully sent via modem to {phone}")
                return True
            print(f"Modem rejected message: {res.text}")
        except Exception as e:
            print(f"Failed to transmit SMS: {e}")
        return False


