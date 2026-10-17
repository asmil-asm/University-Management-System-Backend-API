from django.db.models import Q
from rest_framework import serializers
from .models import University, Language, SocialMedia, Branch, Page, ContactMessage


class UniversityLookupField(serializers.PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        kwargs.setdefault('queryset', University.objects.all())
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if isinstance(data, bool) or data is None:
            self.fail('incorrect_type', data_type=type(data).__name__)

        queryset = self.get_queryset()
        value = str(data).strip()

        if value.isdigit():
            obj = queryset.filter(pk=int(value)).first()
            if obj:
                return obj

        matches = list(
            queryset.filter(Q(name_ar__iexact=value) | Q(name_en__iexact=value))[:2]
        )
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            raise serializers.ValidationError("يوجد أكثر من جامعة بنفس الاسم، استخدم الـ id.")
        raise serializers.ValidationError("لم يتم العثور على جامعة بهذا الـ id أو الاسم.")


class SocialMediaSerializer(serializers.ModelSerializer):
    university = UniversityLookupField()

    class Meta:
        model = SocialMedia
        fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):
    university = UniversityLookupField()

    class Meta:
        model = Branch
        fields = '__all__'


class UniversitySerializer(serializers.ModelSerializer):
    social_links = SocialMediaSerializer(many=True, read_only=True)
    branches = BranchSerializer(many=True, read_only=True)

    class Meta:
        model = University
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class PageSerializer(serializers.ModelSerializer):
    # لا يوجد حقل university في موديل Page
    class Meta:
        model = Page
        fields = '__all__'


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = [
            'id',
            'sender_name',
            'sender_email',
            'subject_ar',
            'subject_en',
            'message_ar',
            'message_en',
            'sent_at',
            'status',
        ]
        read_only_fields = ['sent_at', 'status']