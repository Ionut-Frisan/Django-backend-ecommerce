from lib2to3.pytree import Base
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Email required")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        print(user.email, user.username, user.password)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='email',
                              max_length=60, unique=True, null=False)
    username = models.CharField(max_length=30, unique=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    registration_date = models.DateTimeField(
        verbose_name='registration date', auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = AccountManager()

    def __str__(self):
        return f'{self.email}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_profile_picture(self):
        if self.profile_picture:
            return 'http://127.0.0.1:8000' + self.profile_picture.url
        return ''
