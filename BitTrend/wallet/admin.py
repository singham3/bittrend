from django.contrib import admin
from .models import UserWallet, AccountTransaction, HoldAmount
from django.db.models import Q, Sum


class UserWalletAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "amount", "is_active", "created_at"]


class AccountTransactionAdmin(admin.ModelAdmin):
    list_display = ["id", "paymentId", "PayerID", "user", "email", "first_name", "last_name", "gross_amount", "net_amount", "fees",
                    "admin_fees", "currency", "is_success", "created_at"]


class HoldAmountAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "wallet", "order", "amount", "created_at"]


admin.site.register(AccountTransaction, AccountTransactionAdmin)
admin.site.register(UserWallet, UserWalletAdmin)
admin.site.register(HoldAmount, HoldAmountAdmin)
