from django.db import models


class University(models.Model):
    name_ar = models.CharField(max_length=255, verbose_name="الاسم بالعربية")
    name_en = models.CharField(max_length=255, verbose_name="الاسم بالإنجليزية")
    location = models.CharField(max_length=255, verbose_name="الموقع")
    email = models.EmailField(verbose_name="البريد الإلكتروني")
    phone = models.CharField(max_length=20, verbose_name="الهاتف")
    logo = models.ImageField(upload_to='university/', null=True, blank=True, verbose_name="الشعار")

    def __str__(self):
        return self.name_ar


class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)
    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label


class SocialMedia(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self):
        return f"{self.platform} - {self.university.name_ar}"


class Branch(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=255)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name


class Page(models.Model):
    PAGE_TYPES = (
        ('about', 'عن الجامعة'),
        ('vision', 'الرؤية والرسالة'),
        ('policy', 'السياسات'),
        ('custom', 'صفحة مخصصة'),
    )
    slug = models.SlugField(unique=True)
    title_ar = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    content_ar = models.TextField()
    content_en = models.TextField()
    page_type = models.CharField(max_length=20, choices=PAGE_TYPES, default='custom')

    def __str__(self):
        return self.title_ar

class ContactMessage(models.Model):
    sender_name = models.CharField(max_length=255)
    sender_email = models.EmailField()
    subject = models.CharField(max_length=255, verbose_name="الموضوع", null=True, blank=True)
    message = models.TextField(verbose_name="الرسالة", null=True, blank=True) # أضفنا null و blank
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='new')

    def __str__(self):
        return f"{self.subject} from {self.sender_name}"