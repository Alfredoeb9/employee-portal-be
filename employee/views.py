from django.shortcuts import render
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from employee.serializers import EmployeeSerializer

# Create your views here.
class EmployeeView(CreateAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminUser]

    def post(self, request):
        employee_data = request.data
        serializer = self.serializer_class(data=employee_data)

        if serializer.is_valid():
            serializer.save()
            employee = serializer.data

            return Response({
                'data': employee,
                'message': 'Employee has been created successfully'
            }, status=HTTP_201_CREATED)
        
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)