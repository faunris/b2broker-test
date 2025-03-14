import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .wallets.factories import WalletFactory, TransactionFactory

register(WalletFactory)
register(TransactionFactory)


@pytest.fixture
def drf_client():
    return APIClient()
