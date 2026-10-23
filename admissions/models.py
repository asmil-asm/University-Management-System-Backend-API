from django.db import models

class Student(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    national_id = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, default='accepted') 
    student_file = models.FileField(upload_to='students/', null=True, blank=True)

    def __str__(self):
        return self.full_name

class Admission(models.Model):
    program = models.OneToOneField('academics.Program', on_delete=models.CASCADE, related_name='admission_info')
    requirements_en = models.TextField()
    requirements_ar = models.TextField()
    procedure_en = models.TextField()
    procedure_ar = models.TextField()
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2)
    academic_calendar = models.TextField()

    def __str__(self):
        return f"Admission for {self.program.name_ar}"

class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'قيد الانتظار'),
        ('accepted', 'مقبول'),
        ('rejected', 'مرفوض'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applications')
    program = models.ForeignKey('academics.Program', on_delete=models.CASCADE, related_name='applications')
    apply_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    form_file = models.FileField(upload_to='applications/', null=True, blank=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.program.name_ar}"