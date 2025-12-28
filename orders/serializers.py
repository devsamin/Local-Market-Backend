# from rest_framework import serializers
# from .models import Order, OrderItem
# from products.serializers import ProductSerializer

# class OrderItemSerializer(serializers.ModelSerializer):
#     product = ProductSerializer(read_only=True)

#     class Meta:
#         model = OrderItem
#         fields = ["id", "product", "quantity", "price", "seller"]


# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True, read_only=True)

#     class Meta:
#         model = Order
#         fields = ["id", "user", "total_price", "status", "created_at", "items"]
#         read_only_fields = ["user", "status"]

#     def create(self, validated_data):
#         user = self.context["request"].user
#         return Order.objects.create(user=user, **validated_data)


# orders/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer
from reviews.models import Review
# Serializer for sellers to view their own order items
# class SellerOrderItemSerializer(serializers.ModelSerializer):
#     product = ProductSerializer(read_only=True)
#     buyer_name = serializers.CharField(source='order.user.username', read_only=True)

#     class Meta:
#         model = OrderItem
#         fields = ["id", "product", "quantity", "price", "status"]
#         read_only_fields = ["product", "quantity", "price"]


class SellerOrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    buyer_name = serializers.CharField(source='order.user.username', read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price", "status", "buyer_name", "order"]
        read_only_fields = ["product", "quantity", "price", "order"]

# Serializer for full order (user side)
# class OrderItemSerializer(serializers.ModelSerializer):
#     product = ProductSerializer(read_only=True)

#     class Meta:
#         model = OrderItem
#         fields = ["id", "product", "quantity", "price", "seller", "status"]


# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True, read_only=True)

#     class Meta:
#         model = Order
#         fields = ["id", "user", "total_price", "status", "created_at", "items"]
#         read_only_fields = ["user", "status"]

#     def create(self, validated_data):
#         user = self.context["request"].user
#         return Order.objects.create(user=user, **validated_data)



class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    review = serializers.SerializerMethodField()
    

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price", "seller", "status", "review"]

    def get_review(self, obj):
        review = getattr(obj, "review", None) or Review.objects.filter(order_item=obj).first()
        return {
            "id": review.id,
            "rating": review.rating,
            "comment": review.comment
        } if review else None

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "user", "total_price", "status", "created_at", "items"]

