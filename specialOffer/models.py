from django.db import models
from cloudinary.models import CloudinaryField


class SpecialOffer(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    # image = models.FileField(upload_to="special_offers/" , blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True)
    badge = models.CharField(max_length=100)
    badgeColor = models.CharField(max_length=50, default="bg-green-500")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
