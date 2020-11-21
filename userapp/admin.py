from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django import forms
from rest_framework.authtoken.models import Token
from userapp.models import User, PasswordResetToken, LoginToken, SignupToken
from userapp.models.subscription import Subscription

class UserAdminForm(forms.ModelForm):
    # password = forms.CharField(max_length=64, required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'

    def clean(self):
        from django.contrib.auth.hashers import make_password
        password = self.cleaned_data.get('password')
        if password:
            password = make_password(password)
        else:
            self.cleaned_data.pop('password')
        return self.cleaned_data


class AdminUserapp(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'active', 'admin')
    # readonly_fields = ('password',)
    form = UserAdminForm
    fieldsets = (
            (_("Personal info"), {
                'fields':(
                    'email', 'first_name', 'middle_name',\
                    'last_name', 'gender', 'phone_number', 'image', 'password'
                    )
                }
            ),
            (_("User Address"), {
                'fields':(
                    'country', 'state', 'city', 'address', 'zip_code'
                    )
                }
            ),
            (_("Group"), {
                'fields':(
                    'group',
                    )
                }
            ),
            (_("Permission"), {'fields':('staff',)}),)

class AdminPasswordResetTokenapp(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_used')


class AdminSubscription(admin.ModelAdmin):
    list_display = ('id', 'user', 'email', 'promotion')


admin.site.register(LoginToken)
admin.site.register(PasswordResetToken, AdminPasswordResetTokenapp)
admin.site.register(SignupToken)
admin.site.register(User, AdminUserapp)
admin.site.register(Subscription, AdminSubscription)
admin.site.unregister(Token)
