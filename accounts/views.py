from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from django.shortcuts import get_object_or_404
from .serializers import LoginSerializer
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.core.mail import send_mail

from .models import CustomUser
from .serializers import EmployeeSerializer, EmployeeDetailSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Added by harsh - Admin Dashboard
class IsAdminPermission(permissions.BasePermission):
    """Custom permission to allow only admins to access these endpoints."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class AdminDashboardView(APIView):
    """Returns a list of employees for a given admin"""
    permission_classes = [IsAdminPermission]

    def get(self, request, id):
        admin = get_object_or_404(CustomUser, id=id, role='admin')

        if not admin:
            return Response({"error": "Admin not found"}, status=status.HTTP_404_NOT_FOUND)

        employees = CustomUser.objects.filter(role='employee')
        data = EmployeeSerializer(employees, many=True).data
        return Response({'employees': data}, status=status.HTTP_200_OK)

class EmployeeDetailView(APIView):
    """Returns details of a specific employee"""
    permission_classes = [IsAdminPermission]

    def get(self, request, id, employee_id):
        admin = get_object_or_404(CustomUser, id=id, role='admin')
        employee = get_object_or_404(CustomUser, id=employee_id, role='employee', company_id=admin.company_id)
        data = EmployeeDetailSerializer(employee).data
        return Response(data, status=status.HTTP_200_OK)

def simple_email(request):
    
    send_mail(subject='Test Email',message='you required attention',recipient_list=['test@mail.com'],from_email=['devbawari4@gmail.com'])
    return HttpResponse('Email sent successfully')