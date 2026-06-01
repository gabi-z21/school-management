from django.db import models

# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=50)
    device_user_id = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class AttendanceLog(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    device_log_id = models.IntegerField(unique=True)
    timestamp = models.DateTimeField()


class DailyAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()

    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return (
            f"{self.student.name} - {self.date} - "
            f"{self.check_in} - {self.check_out}"
        )


class SMS(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("sent", "Sent"),
        ("failed", "Failed"),
    ]

    batch_name = models.CharField(max_length=20, blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    message = models.TextField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "SMS Logs"
        ordering = ['-created_at']

    def __str__(self):
        return (
            f"{self.student} - {self.phone} "
            f"({self.status})"
        )