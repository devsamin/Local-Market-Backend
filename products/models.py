from django.db import models
from django.conf import settings
from category.models import Category
from cloudinary.models import CloudinaryField

class Product(models.Model):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products"
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.PositiveIntegerField(default=0)  # Discount in percentage
    stock = models.PositiveIntegerField(default=0)
    # image = models.ImageField(upload_to="products/", blank=True, null=True)
    # image2 = models.ImageField(upload_to="products/", blank=True, null=True)
    # image3 = models.ImageField(upload_to="products/", blank=True, null=True)
    image = CloudinaryField("image", blank=True, null=True)
    image2 = CloudinaryField("image2", blank=True, null=True)
    image3 = CloudinaryField("image3", blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name="products", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_available(self):
        return self.stock > 0 and self.is_approved

    @property
    def discounted_price(self):
        """Calculate discounted price."""
        return self.price - (self.price * self.discount / 100)

    def __str__(self):
        return self.name
