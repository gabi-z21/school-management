from django.core.management.base import BaseCommand
from django.db import close_old_connections
from attendance.models import SMS
from attendance.sms_service import SMSService
import time


class Command(BaseCommand): 
    help = 'Polls the database and sends pending SMS via hardware modem'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting SMS Worker...'))
        sms_service = SMSService(port='COM3')

        while True:
            close_old_connections()
            messages = SMS.objects.filter(status='pending')

            if messages.exists():
                for msg in messages:
                    try:
                        sms_service.send_sms(msg.phone, msg.message)
                        msg.status = 'sent'

                    except Exception:
                        msg.status = 'failed'

                    msg.save()
                    time.sleep(2)

                time.sleep(5)
