from rest_framework import serializers
from .models import College, CollegeImage, Department, Program, AcademicStaff, Research

class ResearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Research
        fields = '__all__'

class AcademicStaffSerializer(serializers.ModelSerializer):
    researches = ResearchSerializer(many=True, read_only=True)
    
    class Meta:
        model = AcademicStaff
        fields = '__all__' 

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    programs = ProgramSerializer(many=True, read_only=True)
    staff = AcademicStaffSerializer(many=True, read_only=True)
    
    class Meta:
        model = Department
        fields = '__all__'

class CollegeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeImage
        fields = ['id', 'image', 'created_at']

class CollegeSerializer(serializers.ModelSerializer):
    departments = DepartmentSerializer(many=True, read_only=True)
    images = CollegeImageSerializer(many=True, read_only=True)
    
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=100, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = College
        fields = '__all__'

    def _extract_images(self, validated_data):
        request = self.context.get('request')
        uploaded_images = validated_data.pop('uploaded_images', [])
        
        if request:
            # البحث الشامل في جميع الاحتمالات الممكنة لمفاتيح الصور القادمة من الـ Frontend
            if not uploaded_images:
                uploaded_images = (
                    request.FILES.getlist('images') or 
                    request.FILES.getlist('uploaded_images') or 
                    request.FILES.getlist('image')
                )
            else:
                # دمج أي صور إضافية قد تكون موجودة في الطلب مباشرة
                extra_images = request.FILES.getlist('images') or request.FILES.getlist('image')
                for img in extra_images:
                    if img not in uploaded_images:
                        uploaded_images.append(img)
                        
        return uploaded_images

    def create(self, validated_data):
        uploaded_images = self._extract_images(validated_data)
        college = College.objects.create(**validated_data)
        for image in uploaded_images:
            CollegeImage.objects.create(college=college, image=image)
        return college

    def update(self, instance, validated_data):
        uploaded_images = self._extract_images(validated_data)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # حفظ كل الصور الجديدة المرفوعة
        for image in uploaded_images:
            CollegeImage.objects.create(college=instance, image=image)
            
        return instance