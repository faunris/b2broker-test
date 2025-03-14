from django.db import models

from wallets.contants import CONSTRAINTS_WALLET_BALANCE_NAME

# TODO: Place for question to analytics.
MONEY_MAX_DIGITS = 18
MONEY_DECIMAL_PLACES = 4


class Wallet(models.Model):
    label = models.CharField(max_length=255, db_index=True)  # TODO: max_length depends on business logic
    balance = models.DecimalField(
        max_digits=MONEY_MAX_DIGITS, decimal_places=MONEY_DECIMAL_PLACES, default=0, db_index=True
    )

    class Meta:
        ordering = ["id"]
        constraints = [
            models.CheckConstraint(condition=models.Q(balance__gte=0), name=CONSTRAINTS_WALLET_BALANCE_NAME),
        ]


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    txid = models.CharField(max_length=255, unique=True, blank=False)  # TODO: max_length depends on business logic
    amount = models.DecimalField(max_digits=MONEY_MAX_DIGITS, decimal_places=MONEY_DECIMAL_PLACES, db_index=True)

    class Meta:
        ordering = ["id"]
