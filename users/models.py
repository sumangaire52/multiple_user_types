from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        SELLER = 'SELLER','seller'
        BUYER = 'BUYER','Buyer'
    
    default_role = Role.BUYER

    email = models.EmailField(_('Email'), max_length=50, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.CharField(_('Role'),max_length=50, choices=Role.choices, default=default_role)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class SellerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role = User.Role.SELLER)


class BuyerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role = User.Role.BUYER)


class Seller(User):
    sellers = SellerManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = User.Role.SELLER
        return super().save(*args, **kwargs)

    class Meta:
        proxy = True


class Buyer(User):
    buyers = BuyerManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = User.Role.BUYER

    class Meta:
        proxy = True