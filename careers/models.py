from django.db import models

class JobPosting(models.Model):
    university = models.ForeignKey('core.University', on_delete=models.CASCADE, related_name='job_postings')
    title_en = models.CharField(max_length=255)
    title_ar = models.CharField(max_length=255)
    job_type = models.CharField(max_length=50) # e.g. Full-time, Part-time
    description_en = models.TextField()
    description_ar = models.TextField()
    requirements_en = models.TextField()
    requirements_ar = models.TextField()
    deadline = models.DateField()
    status = models.CharField(max_length=20, default='open')

    def __str__(self):
        return self.title_en

class JobApplication(models.Model):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    applicant_name = models.CharField(max_length=255)
    applicant_email = models.EmailField()
    cv = models.FileField(upload_to='cvs/')
    apply_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default='received')

    def __str__(self):
        return f"{self.applicant_name} - {self.job.title_en}"