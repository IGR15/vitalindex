from rest_framework import serializers
from staff.models import Department, Doctor, Nurse, Student
from users.models import User
from users.api.serializers import UserSerializer,UserSerializerForPUT

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Doctor
        fields = [
            'doctor_id',
            'user',
            'specialization',
            'license_number',
            'joining_date',
            'department'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'Doctor'
        user = User.objects.create(**user_data)
        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        for attr, value in user_data.items():
             if attr != 'username' and attr != 'role':  
                setattr(user, attr, value)
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    
class DoctorSerializerForPUT(serializers.ModelSerializer):
    user = UserSerializerForPUT(required=True)

    class Meta:
        model = Doctor
        fields = [
            'doctor_id',
            'user',
            'specialization',
            'license_number',
            'joining_date',
            'department'
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        for attr, value in user_data.items():
            if attr != 'username' and attr != 'role':  
                setattr(user, attr, value)
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance



class NurseSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Nurse
        fields = [
            'nurse_id',
            'user',
            'department',
            'assigned_shift'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'Nurse'
        user = User.objects.create(**user_data)
        nurse = Nurse.objects.create(user=user, **validated_data)
        return nurse

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        for attr, value in user_data.items():
            if attr != 'role':
                setattr(user, attr, value)
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Student
        fields = [
            'student_id',
            'user',
            'academic_course',
            'academic_year'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'Student'
        user = User.objects.create(**user_data)
        student = Student.objects.create(user=user, **validated_data)
        return student

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        for attr, value in user_data.items():
            if attr != 'role':
                setattr(user, attr, value)
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
