from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
import uuid

class MainUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    org_name = models.CharField(max_length=50)

    def __str__(self):
        return self.org_name

class Privilage(models.Model):
    visit = models.BooleanField(default = False)
    purchase = models.BooleanField(default = False)
    silver_target_visit = models.IntegerField(blank=True, null=True)
    silver_target_purchase = models.IntegerField(blank=True, null=True)
    silver_offer = models.CharField(max_length=50, blank=True, null=True)
    gold_target_visit = models.IntegerField(blank=True, null=True)
    gold_target_purchase = models.IntegerField(blank=True, null=True)
    gold_offer = models.CharField(max_length=50, blank=True, null=True)
    diamond_target_visit = models.IntegerField(blank=True, null=True)
    diamond_target_purchase = models.IntegerField(blank=True, null=True)
    diamond_offer = models.CharField(max_length=50, blank=True, null=True)
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, blank=True, null=True)
    saved = models.BooleanField(default=False)

class CustomerUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone_number = models.IntegerField()
    def __str__(self):
        return self.name

class CustomerHotelRegister(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=50)
    hotel = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    visit = models.IntegerField(blank=True, null=True)
    purchase = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

class CustomerRecord(models.Model):
    amount = models.IntegerField()
    user = models.ForeignKey(CustomerHotelRegister, on_delete=models.CASCADE)
    hotel = models.ForeignKey(MainUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name
