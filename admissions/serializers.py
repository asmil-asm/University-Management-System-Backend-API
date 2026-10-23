from rest_framework import serializers
from academics.models import Program
from .models import Admission, Application, Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['status']


class AdmissionSerializer(serializers.ModelSerializer):
    program_details = serializers.SerializerMethodField()

    class Meta:
        model = Admission
        fields = '__all__'

    def get_program_details(self, obj):
        from academics.serializers import ProgramSerializer
        return ProgramSerializer(obj.program).data


class ApplicationSerializer(serializers.ModelSerializer):
    student_details = StudentSerializer(source='student', read_only=True)
    program_details = serializers.SerializerMethodField()
    student_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['apply_date']

    def get_program_details(self, obj):
        from academics.serializers import ProgramSerializer
        return ProgramSerializer(obj.program).data

    def update(self, instance, validated_data):
        """
        المنطق الاحترافي في سوق العمل:
        - لا يتم حذف الطلب أبداً (لأنه سجل أرشيفي وقانوني).
        - يتم تحديث حالة الطلب (pending, accepted, rejected).
        - يتم مزامنة حالة الطالب المرتبط تلقائياً بناءً على حالة الطلب.
        """
        status_choice = validated_data.get('status', instance.status)
        student = instance.student

        # 1. تحديث حالة الطلب
        instance.status = status_choice
        instance.save()

        # 2. تحديث حالة الطالب المرتبط بناءً على قرار القبول/الرفض
        if student:
            if status_choice == 'accepted':
                student.status = 'accepted'
                if instance.form_file and not student.student_file:
                    student.student_file = instance.form_file
                student.save()
            elif status_choice == 'rejected':
                student.status = 'rejected'
                student.save(update_fields=['status'])
            elif status_choice == 'pending':
                student.status = 'pending'
                student.save(update_fields=['status'])

        # 3. تحديث اسم الطالب إن وجد في الطلب
        student_name = validated_data.get('student_name')
        if student_name and student:
            student.full_name = student_name
            student.save(update_fields=['full_name'])

        return instance


class ApplicationCreateSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    national_id = serializers.CharField(max_length=20)
    program = serializers.PrimaryKeyRelatedField(queryset=Program.objects.all())
    form_file = serializers.FileField(required=False, allow_null=True)

    def validate(self, attrs):
        qs = Student.objects.filter(national_id=attrs['national_id']).exclude(email=attrs['email'])
        if qs.exists():
            raise serializers.ValidationError(
                {'national_id': 'This national ID is already registered with another email.'}
            )
        return attrs

    def create(self, validated_data):
        form_file = validated_data.get('form_file')
        
        # إنشاء أو تحديث الطالب مع ربط الملف مباشرة بحسابه أيضاً
        student, created = Student.objects.get_or_create(
            email=validated_data['email'],
            defaults={
                'full_name': validated_data['full_name'],
                'national_id': validated_data['national_id'],
                'status': 'pending',
                'student_file': form_file,
            },
        )
        
        if not created:
            student.full_name = validated_data['full_name']
            if not Student.objects.filter(national_id=validated_data['national_id']).exclude(pk=student.pk).exists():
                student.national_id = validated_data['national_id']
            if form_file:
                student.student_file = form_file
            student.save()

        return Application.objects.create(
            student=student,
            program=validated_data['program'],
            form_file=form_file,
            status='pending'
        )

    def to_representation(self, instance):
        return ApplicationSerializer(instance).data