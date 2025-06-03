from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role', 'phone', 'address')}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'role__name')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')

    def save_model(self, request, obj, form, change):
        # Auto-assign 'Admin' role for superuser
        if obj.is_superuser:
            admin_role = Role.objects.filter(name='Admin').first()
            if admin_role:
                obj.role = admin_role
        obj.save()

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
