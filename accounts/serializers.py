from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, Token, TokenError
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_str, smart_bytes, force_str
from django.urls import reverse
from .models import User
from .utils import send_normal_email

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=3, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=3, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'password2')
        extra_kwargs = {'password': {'required': True, 'write_only': True, 'min_length': 3, 'max_length': 68}, 'password2' : {'required': True, 'write_only': True, 'min_length': 3, 'max_length': 68}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Password fields did not match'})
        
        return attrs
    
    def create(self, validated_data):
        del validated_data['password2']
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=3, write_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'full_name', 'access_token', 'refresh_token')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 3, 'max_length': 68}}

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        request = self.context.get('request')

        # check against the database if the user exists
        user = authenticate(request, email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        
        if not user.is_verified:
            raise AuthenticationFailed('Account is not verified')
        
        # if user is found, get the tokens
        user_tokens = user.tokens()

        return {
            'email': user.email,
            'full_name': user.get_full_name,
            'access_token': str(user_tokens.get('access')),
            'refresh_token': str(user_tokens.get('refresh'))
        }
    
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3)

    class Meta:
        model = User
        fields = ('email')

    def validate(self, attrs):
        email = attrs.get('email', '')

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'User with this email does not exist'})
        
        user = User.objects.get(email=email)
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        request = self.context.get('request')
        site_domain = get_current_site(request).domain

        relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

        absurl = f'http://{site_domain}{relative_link}'

        email_body = f'Hello, \nUse the link below to reset your password \n{absurl}'

        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Reset your password'}

        send_normal_email(data)
        
        return attrs
    
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=68, min_length=3, write_only=True)
    confirm_password = serializers.CharField(max_length=68, min_length=3, write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('password', 'confirm_password', 'uidb64', 'token')

    def validate(self, attrs):
        try:

            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id = user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("Rest link is invalid of has expired", 401)
            
            if password != confirm_password:
                raise AuthenticationFailed("Passwords do not match", 401)
            
            user.set_password(password)
            user.save()
            
            return user
        
        except Exception as e:
            raise AuthenticationFailed("The reset link is invalid or has expired", 401)
        
class LogoutUserSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    default_error_message = {
        'bad_token': 'Token is invalid or expired'
    }

    def validate(self, attrs):
        self.token = attrs['refresh_token']
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            return self.fail('Token is invalid or expired')