from django.urls import path
from .views import SpecialOfferListCreateAPIView

urlpatterns = [
    path("", SpecialOfferListCreateAPIView.as_view(), name="special-offers"),
]
