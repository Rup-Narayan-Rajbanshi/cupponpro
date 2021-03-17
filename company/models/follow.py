from django.db import models
from django.utils import timezone
from userapp.models.user import User
from company.models.company import Company
from helpers.models import BaseModel

class Follows(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def to_representation(self, request=None):
        if self:
            return {
                'id': self.id,
                'user': self.user,
                'company': self.company,
                'created_at': self.created_at
            }