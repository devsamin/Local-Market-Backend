# payments/urls.py
from django.urls import path
from .views import create_stripe_checkout
# from .webhooks import stripe_webhook
from .views import payment_success


urlpatterns = [
    path("stripe/checkout/", create_stripe_checkout),
    # path("stripe/webhook/", stripe_webhook),
    path("payment-success/", payment_success),
]
