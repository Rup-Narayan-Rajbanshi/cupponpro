import uuid
from django.db import models
from userapp.models import User

class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField(max_length=50, unique=True)
    promotion = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'subscribers'
        verbose_name_plural = 'subscribers'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email