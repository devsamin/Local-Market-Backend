# from rest_framework import generics, permissions
# from .models import SpecialOffer
# from .serializers import SpecialOfferSerializer

# class SpecialOfferListCreateAPIView(generics.ListCreateAPIView):
#     queryset = SpecialOffer.objects.all().order_by("-created_at")
#     serializer_class = SpecialOfferSerializer

#     # Only sellers can add offers
#     def perform_create(self, serializer):
#         user = self.request.user
#         if user.role != "seller":
#             raise PermissionError("Only sellers can add special offers.")
#         serializer.save()






from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from .models import SpecialOffer
from .serializers import SpecialOfferSerializer

class SpecialOfferListCreateAPIView(generics.ListCreateAPIView):
    queryset = SpecialOffer.objects.all().order_by("-created_at")
    serializer_class = SpecialOfferSerializer
    parser_classes = (MultiPartParser, FormParser)  # ✅ THIS IS THE FIX

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != "seller":
            raise PermissionError("Only sellers can add special offers.")
        serializer.save()
