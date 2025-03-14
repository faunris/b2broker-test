from rest_framework import viewsets, mixins

from wallets.models import Wallet, Transaction
from wallets.serializers import WalletSerializer, TransactionSerializer


class WalletViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    ordering_fields = ["label", "balance"]
    ordering = ["label"]
    filterset_fields = {
        "balance": ("exact", "lt", "gt", "gte", "lte"),
        "label": ("icontains", "iexact", "contains"),
    }


class TransactionViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    ordering_fields = ["txid", "amount"]
    ordering = ["txid"]
    filterset_fields = {
        "amount": ("exact", "lt", "gt", "gte", "lte"),
        "txid": ("exact",),
        "wallet__id": ("exact",),
    }
