from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):  # Custom user model
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set', 
        blank=True,
        help_text='Groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions', 
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    level = models.IntegerField(choices=[
        (1, 'Student'),
        (2, 'Nurse'),
        (3, 'Doctor'),
    ])

    def __str__(self):
        return f"{self.name} (Level {self.level})"

class UserRolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="roles")
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name="permissions")

    class Meta:
        unique_together = ('role', 'permission')
