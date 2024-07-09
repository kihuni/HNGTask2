from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid

class MyUserManager(BaseUserManager):
    def create_user(self, firstName, lastName, email, password=None, phone=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not firstName or not lastName:
            raise ValueError("Users must have a first and last name")
        if not password:
            raise ValueError("Users must have a password")

        user = self.model(
            firstName=firstName,
            lastName=lastName,
            email=self.normalize_email(email),
            phone=phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, firstName, lastName, email, password=None, phone=None):
        user = self.create_user(
            firstName=firstName,
            lastName=lastName,
            email=email,
            password=password,
            phone=phone
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    userId = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Organisation(models.Model):
    orgId = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    users = models.ManyToManyField(User, related_name='organisations')
