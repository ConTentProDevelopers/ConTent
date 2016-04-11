from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.conf import settings

# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name, phone_number):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email),
                          password=password,
                          first_name=first_name,
                          last_name=last_name,
                          phone_number=phone_number)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.model(email=self.normalize_email(email),
                          password=password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=60, blank=True)
    phone_number = models.CharField(max_length=9, blank=True)
    email = models.EmailField(verbose_name='email address',
                              max_length=255,
                              unique=True,)

    email_validated = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser


class FieldOwner(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=50)
    company_NIP = models.CharField(max_length=10)
    company_REGON = models.CharField(max_length=9)
    company_locality = models.CharField(max_length=50)
    company_address = models.CharField(max_length=50)
    company_postal_code = models.CharField(max_length=5)
    account_validated = models.BooleanField(default=False)

    user = models.OneToOneField(settings.AUTH_USER_MODEL)


class Customer(models.Model):
    id = models.AutoField(primary_key=True)

    user = models.OneToOneField(settings.AUTH_USER_MODEL)


class Campsite(models.Model):
    id = models.AutoField(primary_key=True)
    field_name = models.CharField(max_length=100)
    field_locality = models.CharField(max_length=50)
    field_address = models.CharField(max_length=50)
    field_postal_code = models.CharField(max_length=6)
    field_phone_number = models.CharField(max_length=9, blank=True)
    field_email = models.CharField(max_length=100, blank=True)
    field_website = models.CharField(max_length=200, blank=True)
    ratings_number = models.IntegerField(null=True)
    average_rating = models.FloatField(null=True)
    field_photo = models.ImageField(null=True)
    field_description = models.TextField()

    customers = models.ManyToManyField(Customer, through="Rating")
    field_owner = models.ForeignKey(FieldOwner, on_delete=models.CASCADE)


class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.IntegerField()
    comment = models.CharField(max_length=255, blank=True)

    campsite = models.ForeignKey(Campsite, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer)


class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    arrival_date = models.DateField()
    departure_date = models.DateField()
    hour_of_reservation = models.DateTimeField()
    status = models.CharField(max_length=15)

    customer = models.ForeignKey(Customer)
    fieldOwner = models.ForeignKey(FieldOwner)


class Place(models.Model):
    id = models.AutoField(primary_key=True)
    place_type = models.CharField(max_length=50)
    price = models.FloatField()
    dimension = models.FloatField()
    number_of_places = models.IntegerField()
    limit_of_places = models.IntegerField(null=True)

    campsite = models.ForeignKey(Campsite, on_delete=models.CASCADE)
    reservation = models.ManyToManyField(Reservation)


class Convenience(models.Model):
    id = models.AutoField(primary_key=True)
    canteen = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    shower = models.BooleanField(default=False)
    easy_access = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    equipment_rental = models.BooleanField(default=False)

    campsite = models.OneToOneField(Campsite, on_delete=models.CASCADE)


class StaticPage(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    contents = models.TextField()

