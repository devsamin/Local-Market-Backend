from rest_framework import generics, permissions
from .models import Category
from .serializers import CategorySerializer

# ✅ List and Create Category API
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]  # চাইলে IsAuthenticated করতে পারো
