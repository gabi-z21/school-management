from zk import ZK
from datetime import datetime
from django.utils.timezone import make_aware, is_naive
from django.conf import settings
from .models import Student, DailyAttendance, AttendanceLog


DEVICE_IP = getattr(settings, 'ZK_DEVICE_IP', '192.168.1.201')
DEVICE_PORT = 4370


def process_attendance(user_id, timestamp):

    student = Student.objects.filter(device_user_id=user_id).first()
    if not student:
        return
    
    existing = DailyAttendance.objects.filter(
        student=student,
        check_in=timestamp
    ).first()

    if existing:
        print("Already processed this log")
        return

    date = timestamp.date()

    record, _ = DailyAttendance.objects.get_or_create(
        student=student,
        date=date
    )

    # FIRST SCAN
    if record.check_in is None:
        record.check_in = timestamp
        record.save()
        print("CHECK-IN saved")
        return

    # SECOND SCAN
    if record.check_out is None:
        time_diff = (timestamp - record.check_in).total_seconds() / 3600

        if time_diff >= 3:
            record.check_out = timestamp
            record.save()
            print("CHECK-OUT saved")
        else:
            print("Too soon → ignored")

        return


def sync_from_device():

    zk = ZK(DEVICE_IP, port=DEVICE_PORT, timeout=15, force_udp=False)

    conn = None

    try:
        conn = zk.connect()
        print("Connected to device")

        conn.disable_device()
        logs = conn.get_attendance()

        for log in logs:
            print("RAW LOG:", log.__dict__)
           
            user_id = str(log.user_id).strip()
            timestamp = log.timestamp

            if is_naive(timestamp):
                timestamp = make_aware(timestamp)

            student = Student.objects.filter(device_user_id=user_id).first()
            if not student:
                print("Student not found")
                continue

            # 🔥 THIS IS WHERE IT GOES
            exists = AttendanceLog.objects.filter(device_log_id=log.uid).exists()
            if exists:
                print("Skipping already synced log")
                continue

            AttendanceLog.objects.create(
                student=student,
                device_log_id=log.uid,
                timestamp=timestamp
            )

            process_attendance(user_id, timestamp)

        print("Sync completed")

    except Exception as e:
        print("Device sync error:", e)

    finally:
        if conn:
            conn.enable_device()
            conn.disconnect()


