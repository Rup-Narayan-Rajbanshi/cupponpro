import uuid
from django.db import models
from userapp.models.user import  User
from company.models.company import Company
from helpers.models import BaseModel

class Like(BaseModel):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.company.name