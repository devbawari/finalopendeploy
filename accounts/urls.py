from django.urls import path
from .views import LoginView
from .views import AdminDashboardView, EmployeeDetailView, send_healthcare_email, send_emails_to_needy_employees
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('admin-dashboard/<int:id>/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('admin-dashboard/<int:id>/employee/<int:employee_id>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('send-email/', send_healthcare_email, name='send_email'),
    path('employee-needs-care/', send_emails_to_needy_employees, name='employee-needs-care'   )
]
