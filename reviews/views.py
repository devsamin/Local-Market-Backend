from orders.models import OrderItem
from rest_framework.response import Response
# from rest_framework import status
# from rest_framework import viewsets, permissions
# from .models import Review
# from .serializers import ReviewSerializer


# class ReviewViewSet(viewsets.ModelViewSet):
#     queryset = Review.objects.all().order_by("-created_at")
#     serializer_class = ReviewSerializer

#     def get_permissions(self):
#         if self.action in ["create", "update", "destroy"]:
#             return [permissions.IsAuthenticated()]
#         return [permissions.AllowAny()]

#     def create(self, request, *args, **kwargs):
#         user = request.user
#         order_item_id = request.data.get("order_item")

#         if not order_item_id:
#             return Response({"error": "order_item is required"}, status=400)

#         try:
#             order_item = OrderItem.objects.get(id=order_item_id, order__user=user)
#         except OrderItem.DoesNotExist:
#             return Response({"error": "Invalid order item"}, status=400)

#         # ❗ Only allow review if delivered
#         if order_item.status != "delivered":
#             return Response({"error": "You can review only after delivery"}, status=403)

#         # ❗ Prevent duplicate review
#         if hasattr(order_item, "review"):
#             return Response({"error": "Review already submitted"}, status=400)

#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         serializer.save(
#             user=user,
#             product=order_item.product,
#             order_item=order_item
#         )

#         return Response(serializer.data, status=201)


from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        user = self.request.user
        # শুধুমাত্র logged-in user নিজের review দেখতে পারবে
        if user.is_authenticated:
            return Review.objects.filter(user=user).order_by("-created_at")
        return Review.objects.none()  # anonymous user কোন review দেখবে না

    def create(self, request, *args, **kwargs):
        user = request.user
        order_item_id = request.data.get("order_item")

        if not order_item_id:
            return Response({"error": "order_item is required"}, status=400)

        try:
            order_item = OrderItem.objects.get(id=order_item_id, order__user=user)
        except OrderItem.DoesNotExist:
            return Response({"error": "Invalid order item"}, status=400)

        if order_item.status != "delivered":
            return Response({"error": "You can review only after delivery"}, status=403)

        if hasattr(order_item, "review"):
            return Response({"error": "Review already submitted"}, status=400)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=user,
            product=order_item.product,
            order_item=order_item
        )

        return Response(serializer.data, status=201)
