from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
import os
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator


class User(AbstractUser):
    def photo_path(self, filename):
        return os.path.join(f"document/{self.id}/", filename)

    id = models.CharField(max_length=255, primary_key=True, default=get_random_string, editable=False)
    email = models.EmailField(max_length=255, null=True, blank=True)
    mobile = PhoneNumberField(blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    is_mobile = models.BooleanField(default=False)
    is_email = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True)
    token = models.TextField(max_length=20000, null=True, blank=True)
    photo = models.FileField(upload_to=photo_path, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_google_auth = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "User"


class UserAddress(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_address")
    country = models.CharField(max_length=250)
    state = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=250)
    address = models.TextField(max_length=65500)
    pincode = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class UserDocument(models.Model):
    def document_path(self, filename):
        return os.path.join(f"document/{self.user.id}/", filename)

    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_document")
    document_type = models.CharField(max_length=250)
    document1 = models.FileField(upload_to=document_path)
    document2 = models.FileField(upload_to=document_path)
    photo = models.FileField(upload_to=document_path, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="user_document_approved_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class UserAddressProof(models.Model):
    def address_proof_path(self, filename):
        return os.path.join(f"document/{self.user.id}/", filename)

    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_address_proof")
    document_type = models.CharField(max_length=250)
    address_proof1 = models.FileField(upload_to=address_proof_path)
    address_proof2 = models.FileField(upload_to=address_proof_path)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="user_address_proof_approved_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class UserBankAccount(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_bank_account")
    account_no = models.PositiveIntegerField(validators=[MinValueValidator(6)])
    ifsc_code = models.CharField(max_length=50)
    holder_name = models.CharField(max_length=250)
    branch = models.CharField(max_length=250)
    account_type = models.CharField(max_length=50)
    mobile = PhoneNumberField()
    is_default = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="user_bank_account_approved_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
