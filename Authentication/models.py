from django.db.models.base import Model
from django.db.models.fields import BooleanField, EmailField, BigIntegerField, CharField
from django.db.models.fields.related import OneToOneField
from django.db.models import CASCADE
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):
    email = EmailField(max_length=255, unique=True)
    name = CharField(max_length=255)

    is_superuser = BooleanField(default=False)
    is_staff = BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def refresh(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh)

    def access(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh.access_token)

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_superuser


class Two_Factor_Verification(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='twofactor')
    phone_number = BigIntegerField(unique=True,
                                   validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])


class PAN_Verification(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='pan_details')
    pan_number = CharField(unique=True, max_length=10,
                           validators=[RegexValidator(regex='[A-Z]{5}[0-9]{4}[A-Z]{1}',
                                                      message='Invalid PAN',),])
