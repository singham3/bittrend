from django.contrib import admin
from .models import CryptoWallet


class CryptoWalletAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "coin", "address", "is_pool", "created_at"]


admin.site.register(CryptoWallet, CryptoWalletAdmin)
