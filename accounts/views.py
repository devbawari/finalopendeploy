from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from django.shortcuts import get_object_or_404
from .serializers import LoginSerializer
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.http import JsonResponse
import json
from .models import Employeeneedscare
import random   


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

        employees = CustomUser.objects.filter(role='employee')
        serialized_data = EmployeeSerializer(employees, many=True).data

        # Possible moods and activity levels
        moods = ["Happy", "Neutral", "Sad", "Angry", "Depressed"]
        activity_levels = ["Highly Active", "Moderately Active", "Low Activity"]

        enhanced_data = []
        for employee in employees:
            enhanced_data.append({
                "id": employee.id,
                "name": employee.username,
                "email": employee.email,
                "reward_points": random.randint(50, 500),  # Example: Randomized reward points
                "average_working_hours": round(random.uniform(6, 10), 1),  # Example: Random hours
                "leaves_taken": random.randint(0, 20),  # Example: Random leave count
                "activity": random.choice(activity_levels),
                "performance": random.choice(["Excellent", "Good", "Needs Improvement"]),
                "mood": random.choice(moods),
                "original_data": EmployeeSerializer(employee).data  # Include original data
            })

        return Response({'employees': enhanced_data}, status=status.HTTP_200_OK)

class EmployeeDetailView(APIView):
    """Returns details of a specific employee"""
    permission_classes = [IsAdminPermission]

    def get(self, request, id, employee_id):
        admin = get_object_or_404(CustomUser, id=id, role='admin')
        employee = get_object_or_404(CustomUser, id=employee_id, role='employee', company_id=admin.company_id)
        data = EmployeeDetailSerializer(employee).data
        return Response(data, status=status.HTTP_200_OK)



@csrf_exempt
def send_healthcare_email(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            recipient_email = data.get("recipient_email")
            
            if not recipient_email:
                return JsonResponse({"error": "Recipient email is required"}, status=400)

            send_mail(
                subject="Attention",
                message="Healthcare is needed,please contact the hr",
                from_email="devbawari4@example.com",
                recipient_list=[recipient_email]
            )

            return JsonResponse({"message": f"Email successfully sent to {recipient_email}"}, status=200)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt  # Remove this in production and use CSRF token
def send_emails_to_needy_employees(request):
    if request.method == "POST":
        needy_employees = Employeeneedscare.objects.filter(needs_attention=True)

        if not needy_employees.exists():
            return JsonResponse({"message": "No employees need attention"}, status=200)

        failed_emails = []
        
        for employee in needy_employees:
            try:
                send_mail(
                    subject="Attention",
                    message="Healthcare is needed",
                    from_email="devbawari4@example.com",
                    recipient_list=[employee.email]
                )
            except Exception as e:
                failed_emails.append(employee.email)

       
        return JsonResponse({
            "message": f"Emails sent successfully to {needy_employees.count()} employees.",
            "failed_emails": failed_emails
        }, status=200)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)
