# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, first_name, last_name, password=None, **extra_fields):
#         if not email:
#             raise ValueError('Email must be provided')
#         email = self.normalize_email(email)
#         user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
    
#     def create_superuser(self, email,  first_name, last_name, password=None, **extra_fields ):
#         extra_fields.setdefault('is_staff', True )
#         extra_fields.setdefault('is_superuser', True )
#         extra_fields.setdefault('is_active', True )

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(email, first_name, last_name, password, **extra_fields)
    

# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(
#         verbose_name='Email',
#         max_length=180, 
#         unique=True
#         )
#     first_name = models.CharField(max_length=80)
#     last_name = models.CharField(max_length=80)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS= ['first_name', 'last_name' ]
    
#     def __str__(self):
#         return f"{self.first_name}"



from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role='user', **extra_fields):
        
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)

        

        user = self.model(
            
            email=email, 
            role=role, 
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # superuser is always admin
        return self.create_user(email, password, role='admin', **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.role:
            self.role = 'user'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} ({self.role})"

