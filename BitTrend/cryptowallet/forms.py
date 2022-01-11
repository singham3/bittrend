from django import forms
from .models import TestCryptoWallet

type_choices = (
    ("LIMIT", "LIMIT"),
    ("MARKET", "MARKET"),
    ("STOP_LOSS", "STOP_LOSS"),
    ("STOP_LOSS_LIMIT", "STOP_LOSS_LIMIT"),
    ("TAKE_PROFIT", "TAKE_PROFIT"),
    ("TAKE_PROFIT_LIMIT", "TAKE_PROFIT_LIMIT"),
    ("LIMIT_MAKER", "LIMIT_MAKER"),
)


class CreateTestOrderForm(forms.Form):
    symbol = forms.CharField(required=True)
    side = forms.CharField(required=True)
    type = forms.ChoiceField(choices=type_choices, required=True)
    timeInForce = forms.CharField(required=False)
    quantity = forms.FloatField(required=False)
    price = forms.FloatField(required=False)
    newClientOrderId = forms.CharField(required=False)
    stopPrice = forms.CharField(required=False)
    icebergQty = forms.CharField(required=False)
    newOrderRespType = forms.CharField(required=False)
    recvWindow = forms.CharField(required=False)

    class Meta:
        model = TestCryptoWallet
        fields = ['symbol', 'side', 'type', 'timeInForce', 'quantity', 'price', 'newClientOrderId', 'stopPrice', 'icebergQty', 'newOrderRespType',
                  'recvWindow']

    def clean(self):
        cleaned_data = super(CreateTestOrderForm, self).clean()
        return cleaned_data
