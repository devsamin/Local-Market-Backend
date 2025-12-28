# from rest_framework import viewsets, permissions, status
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from .models import Cart, CartItem
# from .serializers import CartSerializer, CartItemSerializer
# from products.models import Product

# class CartViewSet(viewsets.ModelViewSet):
#     serializer_class = CartSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Cart.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     # 🔹 View cart
#     def list(self, request):
#         cart, created = Cart.objects.get_or_create(user=request.user)

#         # Print cart info
#         print(f"Cart ID: {cart.id}, User: {cart.user.username}, Created: {created}")

#         # Print all items in the cart
#         if cart.items.exists():
#             for item in cart.items.all():
#                 print(
#                     f"Item ID: {item.id}, Product: {item.product.name}, "
#                     f"Quantity: {item.quantity}, Total Price: {item.total_price}"
#                 )
#         else:
#             print("Cart is empty")

#         serializer = CartSerializer(cart)
#         return Response(serializer.data)

#     # 🔹 Add item to cart
#     @action(detail=False, methods=['post'])
#     def add_item(self, request):
#         product_id = request.data.get('product_id')
#         quantity = int(request.data.get('quantity', 1))

#         try:
#             product = Product.objects.get(id=product_id)
#         except Product.DoesNotExist:
#             return Response({'error': 'Product not found'}, status=404)

#         cart, created = Cart.objects.get_or_create(user=request.user)

#         # Check stock
#         if product.stock < quantity:
#             return Response({'error': 'Insufficient stock'}, status=400)

#         # Add or update item
#         item, created = CartItem.objects.get_or_create(cart=cart, product=product)
#         item.quantity += quantity
#         item.save()

#         # Reduce stock
#         product.stock -= quantity
#         product.save()

#         # Print updated cart
#         print(f"Added {quantity} of {product.name} to cart.")
#         self.print_cart(cart)

#         return Response({'message': 'Item added successfully'}, status=200)

#     # 🔹 Remove item
#     @action(detail=False, methods=['post'])
#     def remove_item(self, request):
#         product_id = request.data.get('product_id')
#         cart = Cart.objects.get(user=request.user)
#         item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
#         if item:
#             print(f"Removing {item.product.name} from cart.")
#             item.delete()

#             # Print updated cart
#             self.print_cart(cart)

#             return Response({'message': 'Item removed successfully'})
#         return Response({'error': 'Item not found'}, status=404)

#     # 🔹 Clear entire cart
#     @action(detail=False, methods=['post'])
#     def clear(self, request):
#         cart = Cart.objects.get(user=request.user)
#         cart.items.all().delete()

#         print(f"Cleared all items from cart ID: {cart.id}")
#         self.print_cart(cart)

#         return Response({'message': 'Cart cleared successfully'})

#     # 🔹 Utility method to print cart contents
#     def print_cart(self, cart):
#         if cart.items.exists():
#             print(f"Cart ID: {cart.id} contents:")
#             for item in cart.items.all():
#                 print(
#                     f"  Item ID: {item.id}, Product: {item.product.name}, "
#                     f"Quantity: {item.quantity}, Total Price: {item.total_price}"
#                 )
#         else:
#             print("Cart is empty")


from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # ---------------------------------------------------
    # VIEW CART
    # ---------------------------------------------------
    def list(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=200)

    # ---------------------------------------------------
    # ADD ITEM
    # ---------------------------------------------------
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        if quantity <= 0:
            return Response({"error": "Invalid quantity"}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        cart, _ = Cart.objects.get_or_create(user=request.user)

        # STOCK CHECK
        if product.stock < quantity:
            return Response(
                {"error": f"Only {product.stock} items in stock"},
                status=400
            )

        # Add or update cart item
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if created:
            item.quantity = quantity
        else:
            item.quantity += quantity

        item.save()

        # Reduce stock
        product.stock -= quantity
        product.save()

        return Response(
            {"message": "Item added successfully", "cart": CartSerializer(cart).data},
            status=200
        )

    # ---------------------------------------------------
    # REMOVE ONE ITEM COMPLETELY
    # ---------------------------------------------------
    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        product_id = request.data.get("product_id")

        cart = Cart.objects.get(user=request.user)
        item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

        if not item:
            return Response({"error": "Item not found"}, status=404)

        # Restore product stock
        product = item.product
        product.stock += item.quantity
        product.save()

        item.delete()

        return Response(
            {"message": "Item removed successfully", "cart": CartSerializer(cart).data},
            status=200
        )

        # ---------------------------------------------------
    # DECREASE QUANTITY BY 1
    # ---------------------------------------------------
    @action(detail=False, methods=['post'])
    def decrease_item(self, request):
        product_id = request.data.get("product_id")
        cart = Cart.objects.get(user=request.user)
        item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

        if not item:
            return Response({"error": "Item not found"}, status=404)

        # Decrease quantity by 1
        if item.quantity > 1:
            item.quantity -= 1
            item.save()

            # Restore stock by 1
            product = item.product
            product.stock += 1
            product.save()
        else:
            # Quantity is 1 → remove item completely
            product = item.product
            product.stock += 1
            product.save()
            item.delete()

        return Response(
            {"message": "Item quantity decreased", "cart": CartSerializer(cart).data},
            status=200
        )

    # ---------------------------------------------------
    # CLEAR CART
    # ---------------------------------------------------
    @action(detail=False, methods=['post'])
    def clear(self, request):
        cart = Cart.objects.get(user=request.user)

        # Restore stock for all items
        for item in cart.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()

        cart.items.all().delete()

        return Response(
            {"message": "Cart cleared successfully", "cart": CartSerializer(cart).data},
            status=200
        )
