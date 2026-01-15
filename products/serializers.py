# # from rest_framework import serializers
# # from .models import Product
# # from category.models import Category

# # class ProductSerializer(serializers.ModelSerializer):
# #     seller_name = serializers.CharField(source="seller.username", read_only=True)
# #     categories = serializers.PrimaryKeyRelatedField(
# #         many=True, read_only=False, queryset=Category.objects.all()
# #     )

# #     class Meta:
# #         model = Product
# #         fields = [
# #             "id", "seller", "seller_name", "name", "description", "price", "discount",
# #             "stock", "image", "categories", "created_at", "discounted_price"
# #         ]
# #         read_only_fields = ["seller", "created_at", "discounted_price"]



# serializers.py
from rest_framework import serializers
from .models import Product
from category.models import Category
from category.serializers import CategorySerializer  # import nested serializer
from django.db.models import Avg

# class ProductSerializer(serializers.ModelSerializer):
#     seller_name = serializers.CharField(source="seller.username", read_only=True)
#     categories = CategorySerializer(many=True, read_only=True)  # <-- nested serializer

#     class Meta:
#         model = Product
#         fields = [
#             "id", "seller", "seller_name", "name", "description", "price", "discount",
#             "stock", "image", "categories", "created_at", "discounted_price"
#         ]
#         read_only_fields = ["seller", "created_at", "discounted_price"]


class ProductSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source="seller.username", read_only=True)
    average_rating = serializers.SerializerMethodField()
    # Writeable category input
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Category.objects.all(),
        source="categories"
    )

    # Readable nested categories
    categories = CategorySerializer(many=True, read_only=True)

    seller_location = serializers.CharField(source="seller.location", read_only=True)
    image = serializers.SerializerMethodField()
    image2 = serializers.SerializerMethodField()
    image3 = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "seller", "seller_name","seller_location", "name", "description", "price",
            "discount", "stock", "image","image2", "image3",
            "category_ids",                # <-- add this
            "categories",                 # <-- read only nested
            "average_rating",
            "created_at", "discounted_price"
        ]
        read_only_fields = ["seller", "created_at", "discounted_price"]

    # ✅ Cloudinary image URL return
    def get_image(self, obj):
        return obj.image.url if obj.image else None

    def get_image2(self, obj):
        return obj.image2.url if obj.image2 else None

    def get_image3(self, obj):
        return obj.image3.url if obj.image3 else None
    
    def get_average_rating(self, obj):
        result = obj.reviews.aggregate(avg=Avg('rating'))
        return result['avg'] or 0
