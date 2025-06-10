from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser): 
    role = models.CharField(
        max_length=10,
        choices=[
            ('Student', 'Student'),
            ('Nurse', 'Nurse'),
            ('Doctor', 'Doctor')
        ],
        null=True,
        blank=True
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)

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
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @name.setter
    def name(self, value):
        parts = value.split()
        self.first_name = parts[0]
        self.last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
 
# class Permission(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     level = models.IntegerField(choices=[
#         (1, 'Student'),
#         (2, 'Nurse'),
#         (3, 'Doctor'),
#     ])

#     def __str__(self):
#         return f"{self.name} (Level {self.level})"

# class UserRolePermission(models.Model):
#     role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="roles")
#     permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name="permissions")

#     class Meta:
#         unique_together = ('role', 'permission')
