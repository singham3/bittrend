import formtools.preview
from django import forms
from .models import User, UserBankAccount, AbstractUser, UserAddressProof
from django.db.models import Q
from ..gallery.models import Gallery
import os, sys


class UserLoginForm(forms.Form):
    username_or_email = forms.CharField(required=True)
    password = forms.CharField(required=True)
    otp_token = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username_or_email', 'password', 'otp_token']

    def clean(self):
        cleaned_data = super(UserLoginForm, self).clean()
        u_e = cleaned_data['username_or_email']
        if not User.objects.filter(Q(email=u_e) | Q(username=u_e)).exists():
            raise forms.ValidationError("User is not Exists!!!")
        if User.objects.filter(Q(email=u_e) | Q(username=u_e), is_google_auth=True).exists():
            if 'otp_token' not in cleaned_data or not cleaned_data['otp_token']:
                raise forms.ValidationError("otp token is required")
        return cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    parent = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'parent')

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        if "email" in cleaned_data:
            if User.objects.filter(email=cleaned_data['email']).exists():
                raise forms.ValidationError("Email Already Exists !!!")
        if "username" in cleaned_data:
            if User.objects.filter(username=cleaned_data['username']).exists():
                raise forms.ValidationError("username Already Exists !!!")
        if 'parent' in cleaned_data and cleaned_data['parent']:
            if not User.objects.filter(user_id=cleaned_data['parent']).exists():
                raise forms.ValidationError("Parent Code not Exists !!!")
            else:
                cleaned_data['parent'] = User.objects.get(user_id=cleaned_data['parent']).id

        return cleaned_data


class UserProfileForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    date_of_birth = forms.DateField(required=False, input_formats=["%d-%m-%Y"])
    photo = forms.IntegerField(required=False)
    mobile = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'date_of_birth', 'photo', 'mobile')

    def clean(self):
        cleaned_data = super(UserProfileForm, self).clean()
        return cleaned_data


class UserKYCForm(forms.Form):
    name = forms.CharField(required=True)
    country = forms.CharField(required=True)
    city = forms.CharField(required=True)
    address = forms.CharField(required=True)
    pincode = forms.IntegerField(required=True)
    document_type = forms.CharField(required=True)
    document1 = forms.IntegerField(required=True)
    document2 = forms.IntegerField(required=True)
    address_proof_type = forms.CharField(required=True)
    address_proof1 = forms.IntegerField(required=True)
    address_proof2 = forms.IntegerField(required=True)
    photo = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = ('name', 'country', 'city', 'address', 'pincode', 'document_type', 'document1', 'document2',
                  'address_proof_type', 'address_proof1', 'address_proof2', 'photo')

    def clean(self):
        cleaned_data = super(UserKYCForm, self).clean()
        cleaned_data['profile'] = {
            'name': cleaned_data['name'],
        }
        cleaned_data['address'] = {
            'country': cleaned_data['country'],
            'city': cleaned_data['city'],
            'address': cleaned_data['address'],
            'pincode': cleaned_data['pincode'],
        }
        cleaned_data['document'] = {
            'document_type': cleaned_data['document_type'],
            'document1': cleaned_data['document1'],
            'document2': cleaned_data['document2'],
            'photo': cleaned_data['photo']
        }
        cleaned_data['address_proof'] = {
            'document_type': cleaned_data['address_proof_type'],
            'address_proof1': cleaned_data['address_proof1'],
            'address_proof2': cleaned_data['address_proof2'],
        }
        cleaned_data.pop("name")
        cleaned_data.pop("country")
        cleaned_data.pop("city")
        cleaned_data.pop("pincode")
        cleaned_data.pop("document_type")
        cleaned_data.pop("address_proof_type")
        cleaned_data.pop("photo")
        cleaned_data.pop("address_proof1")
        cleaned_data.pop("address_proof2")
        cleaned_data.pop("document1")
        cleaned_data.pop("document2")
        return cleaned_data


class UserBankAccountForm(forms.Form):
    iban = forms.IntegerField(required=True)
    ifsc_code = forms.CharField(required=True)
    holder_name = forms.CharField(required=True)
    branch = forms.CharField(widget=forms.Textarea())
    account_type = forms.CharField(required=True)
    mobile = forms.CharField(required=True)

    class Meta:
        model = UserBankAccount
        fields = ('iban', 'ifsc_code', 'holder_name', 'branch', 'account_type', 'mobile')

    def clean(self):
        cleaned_data = super(UserBankAccountForm, self).clean()
        return cleaned_data
