from django.db import models

class Service(models.Model):
    name_ar = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    service_type = models.CharField(max_length=50)
    url = models.URLField(null=True, blank=True)
    description_ar = models.TextField(null=True, blank=True)
    description_en = models.TextField(null=True, blank=True) 

    def __str__(self):
        return self.name_ar

class Library(models.Model):
    
    university = models.ForeignKey('core.University', on_delete=models.CASCADE, related_name='libraries')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    access_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name