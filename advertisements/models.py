from django.contrib.auth import get_user_model
from django.db import models
from uuid import uuid4
from users.models import User

User = get_user_model()

class Advertisement(models.Model):
    advertisement_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255, null=False, db_index=True)
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    media_file = models.FileField(upload_to='advertisements/', null=True, blank=True)
    url = models.URLField(blank=True, null=True)
    class Type(models.TextChoices):
        IMAGE = 'image', 'image'
        VIDEO = 'video', 'video'
        TEXT = 'text', 'text'

    type = models.CharField(
        max_length = 10,
        choices=Type.choices,
        default = Type.TEXT
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} Advertisement ({self.is_active})"

class AdLike(models.Model):
    """Tracks ad likes"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name="likes")
    liked = models.BooleanField(default=False)
    liked_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'ad')  # One record per user per ad

    def __str__(self):
        return f"{self.user} liked {self.ad} at {self.liked_at}"

class AdView(models.Model):
    """Track ad views"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name="views")
    viewed = models.BooleanField(default=False)  # Track if the ad was seen
    viewed_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'ad')  # One record per user per ad

    def __str__(self):
        return f"{self.user} viewed {self.ad} at {self.viewed_at}"

class AdClick(models.Model):
    """Track add clicks"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name="clicks")
    clicked = models.BooleanField(default=False)  # Track if the ad was clicked
    clicked_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'ad')  # One record per user per ad

class AdSaved(models.Model):
    """Stores ads that users have saved for later"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name="saves")
    saved = models.BooleanField(default=False)  # Track if the ad was saved
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'ad')

    def __str__(self):
        return f"{self.user.username} saved {self.ad.title}"

