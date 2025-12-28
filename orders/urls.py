# from rest_framework.routers import DefaultRouter
# from .views import OrderViewSet

# router = DefaultRouter()
# router.register("", OrderViewSet, basename="order")

# urlpatterns = router.urls



# orders/urls.py
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, SellerOrderViewSet

router = DefaultRouter()
router.register("orders", OrderViewSet, basename="orders")
router.register("seller-orders", SellerOrderViewSet, basename="seller-orders")

urlpatterns = router.urls
