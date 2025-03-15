from django.db import models
from uuid import uuid4

class Advertisement(models.Model):
    advertisement_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255, null=False, db_index=True)
    content = models.TextField(null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    media_file = models.FileField(upload_to='advertisements/', null=True, blank=True)

    class Type(models.TextChoices):
        IMAGE = 'image', 'image'
        VIDEO = 'video', 'video'
        TEXT = 'text', 'text'

    type = models.CharField(
        max_length = 10,
        choices=Type.choices,
        default = Type.TEXT
    )

    def __str__(self):
        return f"{self.title} Advertisement ({self.is_active})"
