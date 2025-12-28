from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# DRF Simple JWT Views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # 🔐 JWT Authentication
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # 👤 User management (signup, login, profile)
    path("api/users/", include("users.urls")),

    # 🛍 Products (CRUD, filtering, etc.)
    path("api/products/", include("products.urls")),

    # 🛒 Cart (add/remove/view cart)
    path("api/cart/", include("cart.urls")),

    # 📦 Orders (create, track, status update)
    path("api/orders/", include("orders.urls")),

    # ⭐ Reviews (rating + comments)
    path("api/reviews/", include("reviews.urls")),

    # 🏷️ Category app
    path("api/category/", include("category.urls")),

    # 📊 Dashboard app
    path("api/dashboard/", include("dashboard.urls")),

    # 🎉 Special Offers (NEW)
    path("api/offers/", include("specialOffer.urls")),

    # 💳 Payments
    path("api/payment/", include("payments.urls")),
]

# 📁 Serve static & media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
