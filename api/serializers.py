from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Employee, CoverShift

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance
    

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'user', 'first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'zip_code', 'date_hired', 'salary', 'job_title', 'department', 'created_at', 'updated_at']
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data):
        print(f'validated_data: {validated_data}')
        print(f'context: {self.context['request'].user}')
        employee = Employee.objects.create(
            user=self.context['request'].user,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            address=validated_data['address'],
            city=validated_data['city'],
            state=validated_data['state'],
            zip_code=validated_data['zip_code'],
            date_hired=validated_data['date_hired'],
            salary=validated_data['salary'],
            job_title=validated_data['job_title'],
            department=validated_data['department']
        )
        return employee
    
    # def update(self, instance, validated_data):
    #     print(f'updated validated_data: {validated_data}')
    #     # instance.user = validated_data.get('user', self.context['request'].user)
    #     instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.last_name = validated_data.get('last_name', instance.last_name)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.phone = validated_data.get('phone', instance.phone)
    #     instance.address = validated_data.get('address', instance.address)
    #     instance.city = validated_data.get('city', instance.city)
    #     instance.state = validated_data.get('state', instance.state)
    #     instance.zip_code = validated_data.get('zip_code', instance.zip_code)
    #     instance.date_hired = validated_data.get('date_hired', instance.date_hired)
    #     instance.salary = validated_data.get('salary', instance.salary)
    #     instance.job_title = validated_data.get('job_title', instance.job_title)
    #     instance.department = validated_data.get('department', instance.department)
    #     # instance.photo = validated_data.get('photo', instance.photo)
    #     instance.save()
    #     return instance
    
class CoverShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverShift
        fields = ['id', 'employee', 'start_date', 'end_date', 'start_time', 'end_time', 'reason', 'created_at', 'updated_at']
        extra_kwargs = {'employee': {'read_only': True}}

    def create(self, validated_data):
        shift = CoverShift.objects.create(**validated_data)
        return shift
    
    # def update(self, instance, validated_data):
    #     instance.start_date = validated_data.get('start_date', instance.start_date)
    #     instance.end_date = validated_data.get('end_date', instance.end_date)
    #     instance.start_time = validated_data.get('start_time', instance.start_time)
    #     instance.end_time = validated_data.get('end_time', instance.end_time)
    #     instance.reason = validated_data.get('reason', instance.reason)
    #     instance.save()
    #     return instance