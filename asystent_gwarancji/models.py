from django.db import models

# Create your models here.

from django.db import models
from django_resized import ResizedImageField

class Receipt(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_purchase = models.DateField()
    date_warranty_to = models.DateField(null=True, blank=True)
    lenght_of_warranty = models.IntegerField()
    status = models.IntegerField(default=1, help_text="0 - Nieaktywny, 1 - Aktywny")
    image = ResizedImageField(null=True, blank=True, quality=75, upload_to="image")
    attachment = models.FileField(upload_to="pdf", null=True, blank=True)

    def __str__(self):
        return f"{self.name}"