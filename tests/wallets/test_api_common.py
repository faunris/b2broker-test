from decimal import Decimal

import pytest


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
def test__wallet__pagination(drf_client, wallet_factory):
    wallet_factory.create_batch(100)

    resp = drf_client.get("/api/wallets/wallet/?page[offset]=5")

    assert resp.status_code == 200, resp.data
    resp_json = resp.json()
    assert len(resp_json["data"]) == 10
    assert resp_json["meta"]["pagination"]["count"] == 100
    assert resp_json["meta"]["pagination"]["limit"] == 10
    assert resp_json["meta"]["pagination"]["offset"] == 5


@pytest.mark.django_db
def test__transaction__pagination(drf_client, transaction_factory):
    transaction_factory.create_batch(100)

    resp = drf_client.get("/api/wallets/transaction/?page[offset]=5")

    assert resp.status_code == 200, resp.data
    resp_json = resp.json()
    assert len(resp_json["data"]) == 10
    assert resp_json["meta"]["pagination"]["count"] == 100
    assert resp_json["meta"]["pagination"]["limit"] == 10
    assert resp_json["meta"]["pagination"]["offset"] == 5


@pytest.mark.django_db
def test__wallet__ordering(drf_client, wallet_factory):
    wallet_factory.create_batch(100)

    resp = drf_client.get("/api/wallets/wallet/?sort=-label")

    assert resp.status_code == 200, resp.data


@pytest.mark.django_db
def test__wallet__filtering(drf_client, wallet_factory):
    wallet_factory.create_batch(100)

    resp = drf_client.get("/api/wallets/wallet/?filter[label.icontains]=test")

    assert resp.status_code == 200, resp.data


@pytest.mark.django_db
def test__transaction__filtering(drf_client, wallet_factory):
    wallet_factory.create_batch(100)

    resp = drf_client.get("/api/wallets/transaction/?filter[wallet.id]=1")

    assert resp.status_code == 200, resp.data
