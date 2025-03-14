from django.urls import path, include

from wallets.urls import router as wallet_router

urlpatterns = [
    path("api/wallets/", include(wallet_router.urls)),
]
