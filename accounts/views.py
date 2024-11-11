from django.shortcuts import render
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from accounts.utils import send_otp_email
from .serializers import UserRegisterSerializer, LoginSerializer, SetNewPasswordSerializer, PasswordResetRequestSerializer, LogoutUserSerializer
from .models import OneTimePassword, User
from employee.models import Employee
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# THIS IS WHAT GETS HIT WHEN A USER REGISTERS

class RegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)

        if serializer.is_valid():
            serializer.save()
            user = serializer.data

            # In production user celery to send email to delay the response
            send_otp_email(user['email'])

            return Response({
                'data': user,
                'message': 'User has been created successfully'
            }, status=HTTP_201_CREATED)
        
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class VerifyUserEmail(GenericAPIView):
    def post(self, request):
        otp_code = request.data.get('otp')

        if not otp_code:
            return Response({'error': 'OTP is required'}, status=HTTP_400_BAD_REQUEST)
        
        try:
            user_otp = OneTimePassword.objects.get(otp=otp_code)
            user = user_otp.user

            if not user.is_verified:
                user.is_verified = True
                user.save()
                Employee.objects.create(user=user)
                return Response({'message': 'User has been verified successfully'}, status=HTTP_201_CREATED)
            
            return Response({'message': 'User is already verified'}, status=HTTP_204_NO_CONTENT)
        
        except OneTimePassword.DoesNotExist:
            return Response({'error': 'Invalid OTP'}, status=HTTP_400_BAD_REQUEST)
        
class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        # pass the request object to the serializer
        serialzer = self.serializer_class(data=request.data, context={'request': request})
        serialzer.is_valid(raise_exception=True)

        return Response(serialzer.data, status=HTTP_200_OK)
    
class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context = {'request': request})
        serializer.is_valid(raise_exception=True)

        return Response({'message': 'Password reset email has been sent'}, status=HTTP_200_OK)
    
class PasswordResetConfirm(GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=HTTP_400_BAD_REQUEST)
            
            return Response({'message': 'Credentials are valid', 'uidb64': uidb64, 'token': token}, status=HTTP_200_OK)
        
        except DjangoUnicodeDecodeError:
            return Response({'error': 'Token is not valid, please request a new one'}, status=HTTP_401_UNAUTHORIZED)
        
class SetNewPassword(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):
            return Response({'message': 'Password has been reset successfully'}, status=HTTP_200_OK)
        
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
class LogoutView(GenericAPIView):
    serializer_class = LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'User has been logged out'}, status=HTTP_204_NO_CONTENT)
        
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)