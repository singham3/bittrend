from django.contrib import admin
from .models import *


class UserAddressAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "country", "state", "city", "pincode", "created_at"]


class UserDocumentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "document_type", "is_approved", "approved_by", "created_at"]


class UserAddressProofAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "document_type", "is_approved", "approved_by", "created_at"]


class UserBankAccountAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "is_approved", "approved_by", "iban", "ifsc_code", "holder_name", "branch", "account_type",
                    "mobile", "created_at"]


admin.site.register(User)
admin.site.register(UserAddress, UserAddressAdmin)
admin.site.register(UserDocument, UserDocumentAdmin)
admin.site.register(UserAddressProof, UserAddressProofAdmin)
admin.site.register(UserBankAccount, UserBankAccountAdmin)
