# # from rest_framework import viewsets, permissions
# # from .models import Product
# # from .serializers import ProductSerializer

# # class ProductViewSet(viewsets.ModelViewSet):
# #     serializer_class = ProductSerializer

# #     def get_queryset(self):
# #         user = self.request.user
# #         if user.is_authenticated:
# #             # Return only this seller’s products
# #             return Product.objects.filter(seller=user).order_by("-created_at")
# #         return Product.objects.none()  # No access if not logged in

# #     def perform_create(self, serializer):
# #         serializer.save(seller=self.request.user)

# #     def get_permissions(self):
# #         if self.action in ["create", "update", "partial_update", "destroy"]:
# #             return [permissions.IsAuthenticated()]
# #         return [permissions.AllowAny()]

# from rest_framework import viewsets, permissions
# from .models import Product
# from .serializers import ProductSerializer

# class ProductViewSet(viewsets.ModelViewSet):
#     serializer_class = ProductSerializer
#     permission_classes = [permissions.AllowAny]  # everyone can access

#     def get_queryset(self):
#         # Show all products to everyone
#         return Product.objects.all().order_by("-created_at")

#     def perform_create(self, serializer):
#         # Only logged-in users can create products
#         if self.request.user.is_authenticated:
#             serializer.save(seller=self.request.user)
#         else:
#             raise PermissionDenied("You must be logged in to create a product.")



from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Product.objects.all().order_by("-created_at")
        seller_id = self.request.query_params.get("seller_id")
        # print("DEBUG seller_id received:", seller_id)
        # Only allow real numeric seller IDs
        if seller_id and seller_id.isdigit():
            queryset = queryset.filter(seller_id=int(seller_id))

        return queryset

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to create a product.")

        serializer.save(seller=self.request.user)
