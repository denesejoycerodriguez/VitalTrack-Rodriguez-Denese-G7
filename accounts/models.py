from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("role", CustomUser.Role.ADMIN)
        return super().create_superuser(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        NURSE = "NURSE", "School Nurse"
        ADMIN = "ADMIN", "Administrator"

    email = models.EmailField(unique=True)  
    role = models.CharField(
        max_length=15,
        choices=Role.choices,
        default=Role.NURSE,  
    )
    contact_number = models.CharField(max_length=20, blank=True)
    profile_photo = models.ImageField(upload_to="profiles/", blank=True, null=True)

    objects = CustomUserManager()

    @property
    def is_nurse(self):
        return self.role == self.Role.NURSE

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"