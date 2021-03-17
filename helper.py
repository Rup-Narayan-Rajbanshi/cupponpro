from userapp.models.user import User
from company.models.company import Company, CompanyUser

def isCompanyUser(user_id, company_id):
    # user_obj = User.objects.filter(id=user_id)
    # company_obj = Company.objects.filter(id=company_id)
    # if user_obj and company_obj:
    # checking if the user belongs to the company users.
    company_user_obj = CompanyUser.objects.filter(user__id=user_id, company__id=company_id)
    if company_user_obj:
            return True
    return False
