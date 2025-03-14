from rest_framework import routers

from wallets.viewsets import WalletViewSet, TransactionViewSet

router = routers.DefaultRouter()
router.register(r"wallet", WalletViewSet)
router.register(r"transaction", TransactionViewSet)
