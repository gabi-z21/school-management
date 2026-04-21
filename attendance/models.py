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