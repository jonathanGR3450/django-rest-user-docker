from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group
from django.conf import settings
import os
import uuid


class UserManager(BaseUserManager):
    """ clase helper manejadora del modelo user """

    def create_user(self, email, password=None, **params):
        ''' crear usuario '''
        if not email:
            raise ValueError('the field email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **params)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        ''' crear usuario superusuario '''
        if not password:
            raise ValueError('the filed password is required')
        user = self.create_user(email=email, password=password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Modelo usuario """
    email = models.EmailField(max_length=255, verbose_name='Correo Electronico', unique=True)
    name = models.CharField(max_length=100, verbose_name='Nombre')
    is_active = models.BooleanField(default=True, verbose_name='Usuario Activo')
    is_staff = models.BooleanField(default=False, verbose_name='Usuario Staff')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creacion')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha Actualizacion')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


class Country(models.Model):
    """ model country """
    name = models.CharField(max_length=255, verbose_name='Nombre')
    code = models.IntegerField()

    def __str__(self):
        return self.name


class State(models.Model):
    """ model country """
    name = models.CharField(max_length=255, verbose_name='Nombre')
    code = models.IntegerField()

    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='states')

    def __str__(self):
        return self.name


class City(models.Model):
    """ model country """
    name = models.CharField(max_length=255, verbose_name='Nombre')
    code = models.IntegerField()

    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Citizen(models.Model):
    """ model citizen """
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    address = models.CharField(max_length=30)
    phone = models.BigIntegerField()
    no_identification = models.BigIntegerField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
