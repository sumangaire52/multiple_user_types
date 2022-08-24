from django.contrib.auth.models import BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extrafields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("Password can not be empty")
        email = self.normalize_email(email)
        user = self.model(email=email, **extrafields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extrafields):
        extrafields.setdefault('is_superuser',True)
        extrafields.setdefault('is_staff',True)
        user = self.create_user(email, password, **extrafields)
        return user
