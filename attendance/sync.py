from datetime import datetime
from zk import ZK
from django.utils.timezone import make_aware
from django.conf import settings
from .models import Student, DailyAttendance


DEVICE_IP = getattr(settings, 'ZK_DEVICE_IP', '192.168.0.121')
DEVICE_PORT = 4370


def process_attendance(user_id, timestamp):
    student = Student.objects.filter(device_user_id=user_id).first()
    if not student:
        print(f"Warning: User ID {user_id} not found in database.")
        return

    date = timestamp.date()

    record, created = DailyAttendance.objects.get_or_create(
        student=student,
        date=date
    )

    if record.check_in is None:
        record.check_in = timestamp
    else: 
        time_diff = timestamp - record.check_in
        if time_diff.total_seconds() > 3600:
            record.check_out = timestamp
        return

    record.save()


def mock_test():
    fake_logs = [
        {"user_id": "G123", "timestamp": "2026-04-21 06:43:00"},
        {"user_id": "G123", "timestamp": "2026-04-21 15:30:00"},
        {"user_id": "A12345", "timestamp": "2026-04-21 08:00:00"},
        {"user_id": "B11111", "timestamp": "2026-04-21 08:10:00"},
    ]

    for log in fake_logs:
        timestamp = datetime.strptime(log["timestamp"], "%Y-%m-%d %H:%M:%S")
        timestamp = make_aware(timestamp)

        process_attendance(log["user_id"], timestamp)


def sync_from_device():

    zk = ZK(DEVICE_IP, port=DEVICE_PORT, timeout=15, force_udp=True)

    conn = None

    try:
        conn = zk.connect()
        print("Connected to device")

        logs = conn.get_attendance()

        for log in logs:
            user_id = str(log.user_id).strip()

            timestamp = log.timestamp
            timestamp = make_aware(timestamp)

            process_attendance(user_id, timestamp)

        print("Sync completed")

    except Exception as e:
        print("Device sync error:", e)

    finally:
        if conn:
            conn.disconnect()


