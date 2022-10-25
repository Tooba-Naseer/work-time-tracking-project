from django.db import models


class TimeStampModel(models.Model):
    """Abstract model that provides timestamp fields"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
