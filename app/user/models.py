import os
import uuid
from functools import partial
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group, 
    Permission
)

def model_image_file_path(instance, filename, model=None):
    """Generate file path for new recipe image"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', model, filename)


class Role(models.Model):
    title = models.CharField(max_length=255)


class UserManager(BaseUserManager):
    """Management class for creating users"""

    def create_user(self, username, email, password=None, **extrafields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError(
                'An email address is required for user registration.'
            )
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extrafields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_staff_user(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

   


class User(AbstractBaseUser, PermissionsMixin):
    """Model for custom definition of system user fields"""
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Change this to a unique name
        blank=True,
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # Change this to a unique name
        blank=True,
    )
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    firstname = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    avatar = models.ImageField(
        null=True, 
        upload_to=partial(model_image_file_path, model='user')
    )
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    role =  models.ForeignKey(Role, on_delete=models.CASCADE)

    objects = UserManager()

    USERNAME_FIELD = 'username'
