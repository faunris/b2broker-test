from decimal import Decimal

import pytest

from wallets.models import Wallet


def wallet_data(label: str, balance: Decimal | None = None, idx: int | None = None):
    data = {
        "data": {
            "type": "Wallet",
            "attributes": {
                "label": label,
            },
        }
    }
    if balance is not None:
        data["data"]["attributes"]["balance"] = balance
    if idx is not None:
        data["data"]["id"] = idx
    return data


def post_transaction_data(txid: str, amount: Decimal, wallet_id: int):
    return {
        "data": {
            "type": "Transaction",
            "attributes": {
                "txid": txid,
                "amount": amount,
            },
            "relationships": {"wallet": {"data": {"type": "Wallet", "id": wallet_id}}},
        }
    }


@pytest.mark.django_db
def test__wallet__get(drf_client, wallet_factory):
    wallet = wallet_factory()

    resp = drf_client.get("/api/wallets/wallet/")

    assert resp.status_code == 200
    assert resp.json()["data"][0]["attributes"]["balance"] == str(wallet.balance)


@pytest.mark.django_db
def test__wallet__create(drf_client):
    resp = drf_client.post("/api/wallets/wallet/", wallet_data("wallet 1", 100))

    assert resp.status_code == 201
    assert resp.json()["data"]["attributes"]["label"] == "wallet 1"
    assert resp.json()["data"]["attributes"]["balance"] == "0.0000"


@pytest.mark.django_db
def test__wallet__update(drf_client, wallet_factory):
    wallet = wallet_factory()

    resp = drf_client.put(f"/api/wallets/wallet/{wallet.id}/", wallet_data("wallet 1", 100, wallet.id))

    assert resp.status_code == 200, resp.data
    assert resp.json()["data"]["attributes"]["label"] == "wallet 1"
    assert resp.json()["data"]["attributes"]["balance"] == str(wallet.balance)


@pytest.mark.django_db
def test__transaction__get(drf_client, transaction_factory):
    transaction = transaction_factory()

    resp = drf_client.get("/api/wallets/transaction/")

    assert resp.status_code == 200
    assert resp.json()["data"][0]["attributes"]["amount"] == str(transaction.amount)


@pytest.mark.django_db
def test__transaction__create(drf_client, wallet_factory):
    wallet = wallet_factory(balance=100)

    drf_client.post("/api/wallets/transaction/", post_transaction_data("test", 100, wallet.id))
    drf_client.post("/api/wallets/transaction/", post_transaction_data("test1", 50, wallet.id))
    resp = drf_client.post("/api/wallets/transaction/", post_transaction_data("test2", -250, wallet.id))

    assert resp.status_code == 201, resp.data
    wallet = Wallet.objects.get(id=wallet.id)
    assert wallet.balance == 0


@pytest.mark.django_db
def test__transaction__create__balance_error(drf_client, wallet_factory):
    wallet = wallet_factory(balance=50)

    resp = drf_client.post("/api/wallets/transaction/", post_transaction_data("test", -100, wallet.id))

    assert resp.status_code == 400, resp.data
    assert resp.json()["errors"][0]["detail"] == "insufficient wallet balance"
    wallet = Wallet.objects.get(id=wallet.id)
    assert wallet.balance == 50
