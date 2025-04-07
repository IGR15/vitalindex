from rest_framework import serializers
from staff.models import (Department,
                          Doctor,
                          Nurse,
                          Student)
from users.models import User


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        
class DoctorSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)  # Get the related User ID
    username = serializers.CharField(source='user.username', required=True)
    email = serializers.EmailField(source='user.email', required=True)
    phone = serializers.CharField(source='user.phone', required=False, allow_null=True)
    address = serializers.CharField(source='user.address', required=False, allow_null=True)
    
    class Meta:
        model = Doctor
        fields = [
            'doctor_id', 'user_id', 'username', 'email', 'phone', 'address',
            'specialization', 'license_number', 'joining_date', 'department'
        ]

    def create(self, validated_data):
        """
        Override create method to ensure User instance is created first.
        """
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor

    def update(self, instance, validated_data):
        """
        Override update method to update both User and Doctor models.
        """
        user_data = validated_data.pop('user', {})
        user = instance.user

        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
    

class NurseSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', required=True)
    email = serializers.EmailField(source='user.email', required=True)
    phone = serializers.CharField(source='user.phone', required=False, allow_null=True)
    address = serializers.CharField(source='user.address', required=False, allow_null=True)

    class Meta:
        model = Nurse
        fields = [
            'nurse_id', 'user_id', 'username', 'email', 'phone', 'address',
            'department', 'assigned_shift'
        ]

    def create(self, validated_data):
        """
        Create a User first, then link it to the Nurse model.
        """
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        nurse = Nurse.objects.create(user=user, **validated_data)
        return nurse

    def update(self, instance, validated_data):
        """
        Update both User and Nurse models.
        """
        user_data = validated_data.pop('user', {})
        user = instance.user

        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class StudentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', required=True)
    email = serializers.EmailField(source='user.email', required=True)
    phone = serializers.CharField(source='user.phone', required=False, allow_null=True)
    address = serializers.CharField(source='user.address', required=False, allow_null=True)

    class Meta:
        model = Student
        fields = [
            'student_id', 'user_id', 'username', 'email', 'phone', 'address',
            'academic_course', 'academic_year'
        ]

    def create(self, validated_data):
        """
        Create a User first, then link it to the Student model.
        """
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        student = Student.objects.create(user=user, **validated_data)
        return student

    def update(self, instance, validated_data):
        """
        Update both User and Student models.
        """
        user_data = validated_data.pop('user', {})
        user = instance.user

        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
