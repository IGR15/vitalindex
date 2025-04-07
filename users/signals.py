from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Role, Permission, UserRolePermission

@receiver(post_save, sender=Role)
def assign_default_permissions(sender, instance, created, **kwargs):
    if created:
        default_permissions = {
            'Doctor': ['View Records', 'Edit Records'],
            'Nurse': ['View Records'],
            'Student': ['View Records'],
        }

        role_name = instance.name
        permissions_to_assign = default_permissions.get(role_name, [])

        for perm_name in permissions_to_assign:
            try:
                perm = Permission.objects.get(name=perm_name)
                UserRolePermission.objects.get_or_create(role=instance, permission=perm)
            except Permission.DoesNotExist:
                continue  
