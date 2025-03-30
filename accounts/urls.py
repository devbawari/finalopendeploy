from django.urls import path
from .views import LoginView
from .views import AdminDashboardView, EmployeeDetailView, simple_email


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('admin-dashboard/<int:id>/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('admin-dashboard/<int:id>/employee/<int:employee_id>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('send-email/', simple_email, name='send-email'),
]
