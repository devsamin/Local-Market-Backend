from rest_framework import serializers
from .models import SpecialOffer

class SpecialOfferSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = SpecialOffer
        fields = "__all__"
