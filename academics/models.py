from django.db import models

class College(models.Model):
    university = models.ForeignKey(
        'core.University', 
        on_delete=models.CASCADE, 
        related_name='colleges',
        null=True, 
        blank=True
    )
    name_ar = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    description_ar = models.TextField(null=True, blank=True)
    description_en = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name_ar

class CollegeImage(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='colleges/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.college.name_ar}"

class Department(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='departments')
    name_ar = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)

    def __str__(self):
        return self.name_ar

class Program(models.Model):
    LEVEL_CHOICES = (
        ('bachelor', 'بكالوريوس'),
        ('master', 'ماجستير'),
        ('phd', 'دكتوراه'),
        ('diploma', 'دبلوم'),
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='programs')
    name_ar = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    study_plan = models.FileField(upload_to='study_plans/', null=True, blank=True)

    def __str__(self):
        return self.name_ar

class AcademicStaff(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='staff')
    full_name = models.CharField(max_length=255)
    title_ar = models.CharField(max_length=100, null=True, blank=True)
    title_en = models.CharField(max_length=100, null=True, blank=True)
    bio_ar = models.TextField(null=True, blank=True)
    bio_en = models.TextField(null=True, blank=True)
    email = models.EmailField()
    staff_type = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='staff/', null=True, blank=True)
    
    # الحقل الجديد لإضافة صورة واحدة مستقلة
    image = models.ImageField(upload_to='staff_images/', null=True, blank=True)

    def __str__(self):
        return self.full_name

class Research(models.Model):
    staff = models.ForeignKey(AcademicStaff, on_delete=models.CASCADE, related_name='researches')
    title_ar = models.CharField(max_length=500, null=True, blank=True)
    title_en = models.CharField(max_length=500, null=True, blank=True)
    abstract_ar = models.TextField(null=True, blank=True)
    abstract_en = models.TextField(null=True, blank=True)
    published_date = models.DateField()
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title_ar or "Research"