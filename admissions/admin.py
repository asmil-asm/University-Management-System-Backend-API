from django.contrib import admin

from .models import Admission, Application, Student

admin.site.register(Student)
admin.site.register(Admission)
admin.site.register(Application)
