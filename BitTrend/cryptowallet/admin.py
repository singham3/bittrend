from django.contrib import admin
from .models import CryptoWallet, TestCryptoWallet, DepositHistory
from django.utils.safestring import mark_safe
import json


class CryptoWalletAdmin(admin.ModelAdmin):
    def network_addresses(self, obj):
        if obj.network_address:
            html = '<ul style="list-style-type:none;">'
            for i in eval(obj.network_address):
                if 'address' in i and i['address']:
                    html += f"""<li style="float:left;list-style-type:none;padding: 0px 25px 0px 0px;">{i['network']}</li>
                            <li style="list-style-type:none;">{i['address']}</li>"""
            return mark_safe(html)

    list_display = ["id", "user", "coin", "address", "network_addresses", "balance", "is_pool", "created_at"]
    search_fields = ['user__email', 'coin']


class TestCryptoWalletAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "coin", "balance", "is_pool", "created_at"]


class DepositHistoryAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "coin", "txId", "address", "amount", "network", "insertTime"]


admin.site.register(CryptoWallet, CryptoWalletAdmin)
admin.site.register(TestCryptoWallet, TestCryptoWalletAdmin)
admin.site.register(DepositHistory, DepositHistoryAdmin)
