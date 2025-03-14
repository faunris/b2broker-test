import factory

from wallets import models


class WalletFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Wallet

    label = factory.Faker("name")
    balance = factory.Faker("pydecimal", positive=True, left_digits=14, right_digits=4)


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Transaction

    wallet = factory.SubFactory(WalletFactory)
    txid = factory.Faker("name")
    amount = factory.Faker("pydecimal", positive=True, left_digits=14, right_digits=4)
