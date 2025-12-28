from rest_framework import serializers
from .models import Review
from products.serializers import ProductSerializer
# class ReviewSerializer(serializers.ModelSerializer):
#     product = ProductSerializer(read_only=True)  # product info nested
#     class Meta:
#         model = Review
#         fields = "__all__"
#         read_only_fields = ["user"]

#     def create(self, validated_data):
#         user = self.context["request"].user
#         return Review.objects.create(user=user, **validated_data)

class ReviewSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["user"]
