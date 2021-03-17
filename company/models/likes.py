import uuid
from django.db import models
from userapp.models.user import  User
from company.models.company import Company

class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company.name