from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('company_id', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('company_id', 'role')}),
    )
    list_display = ['username', 'email', 'company_id', 'role', 'is_staff']
    search_fields = ['username', 'email', 'company_id']

admin.site.register(CustomUser, CustomUserAdmin)
