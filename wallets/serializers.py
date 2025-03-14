from django.db import transaction, IntegrityError
from django.db.models import F
from rest_framework_json_api import serializers

from wallets.contants import CONSTRAINTS_WALLET_BALANCE_NAME
from wallets.models import Wallet, Transaction

WALLET_BALANCE_ERROR = "insufficient wallet balance"


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"
        read_only_fields = ["balance"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def validate(self, attrs):
        value = super().validate(attrs)
        if value["wallet"].balance + value["amount"] < 0:
            raise serializers.ValidationError(WALLET_BALANCE_ERROR)
        return value

    def save(self, **kwargs):
        # In case of parallel requests, we could pass validate check of wallet's balance
        # To test after edit logic, comment validate function
        try:
            super().save(**kwargs)
        except IntegrityError as e:
            if f'violates check constraint "{CONSTRAINTS_WALLET_BALANCE_NAME}"' in str(e):
                raise serializers.ValidationError(WALLET_BALANCE_ERROR)
            raise e

    def create(self, validated_data):
        with transaction.atomic():
            instance = super().create(validated_data)
            Wallet.objects.update(id=instance.wallet_id, balance=F("balance") + instance.amount)
        return instance
