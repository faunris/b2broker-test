# b2broker-test

# Start up

```
docker-compose up
```

### Get wallets
```
curl "http://localhost:8000/api/wallets/wallet/"
```
### Create wallet
```
curl -X "POST" "http://localhost:8000/api/wallets/wallet/" \
     -H 'Content-Type: application/vnd.api+json' \
     -d $'{"data": {
    "type": "Wallet",
    "attributes": {
       "label": "test wallet"
    }
}
}'
```
### Get transactions
```
curl "http://localhost:8000/api/wallets/transaction/"
```
### Create transaction
```
curl -X "POST" "http://localhost:8000/api/wallets/transaction/" \
     -H 'Content-Type: application/vnd.api+json' \
     -d $'{
"data": {
    "type": "Transaction",
    "attributes": {
       "amount": 100,
       "txid": "GDKPBlAoAYdsHOqllsaDDqaBBDqhyirH"
    },
    "relationships": {"wallet": {"data": {"type": "Wallet", "id": 1}}}
}
}'
```

# Local run
```
pyenv local 3.13.1
poetry install
docker-compose -f dev.compose.yaml up -d
poetry run pytest
poetry run make lint
```
