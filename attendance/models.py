from django.db import models

# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=50)
    device_user_id = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    

class DailyAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()

    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'date')
        
    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.check_in} - {self.check_out}"


class SMS (models.Model):
    batch_name = models.CharField(max_length=20)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    message = models.TextField()
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.phone} - {self.message} - {self.status} - {self.created_at}"