from rest_framework import serializers
from .models import SpecialOffer

class SpecialOfferSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = SpecialOffer
        fields = "__all__"
    def get_image(self, obj):
        return obj.image.url if obj.image else None
