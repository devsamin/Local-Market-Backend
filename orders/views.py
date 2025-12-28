# from rest_framework import viewsets, permissions
# from .models import Order
# from .serializers import OrderSerializer

# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all().order_by("-created_at")
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user)

# from rest_framework import viewsets, permissions
# from .models import OrderItem
# from .serializers import OrderItemSerializer

# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = OrderItem.objects.all().order_by("-order__created_at")
#     serializer_class = OrderItemSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         seller_id = self.request.user.id  # Logged-in seller
#         return OrderItem.objects.filter(seller=seller_id)
    


# update code 
# orders/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, SellerOrderItemSerializer

from cart.models import Cart, CartItem
from rest_framework.decorators import action
# -----------------------------
# Seller Dashboard API
# -----------------------------
# class SellerOrderViewSet(viewsets.ModelViewSet):
#     serializer_class = SellerOrderItemSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         # Only return items for the logged-in seller
#         return OrderItem.objects.filter(seller=self.request.user).order_by("-order__created_at")

#     def update(self, request, *args, **kwargs):
#         # Allow seller to update status of their order item
#         instance = self.get_object()
#         status_value = request.data.get("status")

#         if status_value not in dict(OrderItem.STATUS_CHOICES).keys():
#             return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

#         instance.status = status_value
#         instance.save()

#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)


class SellerOrderViewSet(viewsets.ModelViewSet):
    serializer_class = SellerOrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(seller=self.request.user).order_by("-order__created_at")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        status_value = request.data.get("status")

        if status_value not in dict(OrderItem.STATUS_CHOICES).keys():
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        # 1️⃣ Update item status
        instance.status = status_value
        instance.save()

        # 2️⃣ Check if ALL items of the order are delivered
        order = instance.order
        all_items = order.items.all()

        if all(item.status == "delivered" for item in all_items):
            order.status = "delivered"
            order.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

# -----------------------------
# User Order API
# -----------------------------
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return orders for the logged-in user
        return Order.objects.filter(user=self.request.user).order_by("-created_at")
    
    # ---------------------
    # CREATE ORDER FROM CART
    # ---------------------
    # @action(detail=False, methods=["post"], url_path="checkout")
    # def checkout(self, request):
    #     user = request.user

    #     try:
    #         cart = Cart.objects.get(user=user)
    #     except Cart.DoesNotExist:
    #         return Response({"error": "Cart is empty"}, status=400)

    #     cart_items = CartItem.objects.filter(cart=cart)

    #     if not cart_items.exists():
    #         return Response({"error": "No items in cart"}, status=400)

    #     # Calculate total price
    #     total_price = sum(item.product.discounted_price * item.quantity for item in cart_items)

    #     # 1️⃣ Create Order
    #     order = Order.objects.create(user=user, total_price=total_price)

    #     # 2️⃣ Create OrderItems
    #     for item in cart_items:
    #         OrderItem.objects.create(
    #             order=order,
    #             product=item.product,
    #             seller=item.product.seller,  # seller from product model
    #             quantity=item.quantity,
    #             price=item.product.discounted_price,
    #         )

    #     # 3️⃣ Clear the cart
    #     cart_items.delete()

    #     serializer = OrderSerializer(order)
    #     return Response({"message": "Order created successfully", "order": serializer.data})
    @action(detail=False, methods=["post"], url_path="checkout")
    def checkout(self, request):
        user = request.user

        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            return Response({"error": "No items in cart"}, status=400)

        total_price = sum(item.product.discounted_price * item.quantity for item in cart_items)

        # 🔴 Order only CREATED, NOT CONFIRMED
        order = Order.objects.create(
            user=user,
            total_price=total_price,
            payment_method="stripe",
            is_paid=False
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                seller=item.product.seller,
                quantity=item.quantity,
                price=item.product.discounted_price,
            )

        # ❌ DO NOT clear cart here

        return Response({
            "order_id": order.id,
            "total_price": order.total_price
        }, status=201)
