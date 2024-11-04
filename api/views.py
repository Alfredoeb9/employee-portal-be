from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework import generics, status
from .serializers import EmployeeSerializer, CoverShiftSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Employee, CoverShift

# You cannot call this route unless your are JWT TOKEN authenticated
class EmployeeListCreateView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [AllowAny]

    # def get_queryset(self):
    #     return Employee.objects.filter(user=self.request.user)

    # def perform_create(self, serializer):
    #     if serializer.is_valid():
    #         serializer.save(user=self.request.user)
    #     else:
    #         return Response(serializer.errors, status=400)
        
# class EmployeeDelete(generics.DestroyAPIView):
#     serializer_class = EmployeeSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Employee.objects.filter(user=self.request.user)

class CoverShiftDetail(generics.ListCreateAPIView):
    queryset = CoverShift.objects.all()
    serializer_class = CoverShiftSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return CoverShift.objects.all()
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(employee=self.request.user)
        else:
            return Response(serializer.errors, status=400)

class CoverShiftDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = CoverShift.objects.all()
    serializer_class = CoverShiftSerializer


    # def get(self, request, format=None):
    #     snippet = CoverShift.objects.all()
    #     serializer = CoverShiftSerializer(snippet, many=True)
    #     return Response(serializer.data)
    
    # def perform_create(self, serializer):
    #     if serializer.is_valid():
    #         serializer.save(user=self.request.user)
    #     else:
    #         return Response(serializer.errors, status=400)
        
    # def post(self, request, format=None):
    #     serializer = CoverShiftSerializer(data=request.data)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=400)

    # def get_queryset(self):
    #     return Employee.objects.filter(user=self.request.user)

    # def perform_create(self, serializer):
    #     if serializer.is_valid():
    #         serializer.save(user=self.request.user)
    #     else:
    #         return Response(serializer.errors, status=400)
# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

@api_view(['GET'])
def get_message(request):
    return Response({'message': 'Hello, world!'})