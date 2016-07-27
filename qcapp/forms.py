from django import forms
# from django.core import validators
from django.contrib.auth.models import User
from qcapp.models import Reagent
from django.forms import DateField


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=30, required=True)
    password1 = forms.CharField(max_length=60, required=True)
    password2 = forms.CharField(max_length=60, required=True)

    # def isValidUsername(self, field_data, all_data):
    #     try:
    #         User.objects.get(username=field_data)
    #     except User.DoesNotExist:
    #         return
    #     raise validators.ValidationError('The username "%s" is already taken.' % field_data)

    def save(self, new_data):
        u = User.objects.create_user(new_data['username'],
                                     new_data['email'],
                                     new_data['password1'])
        u.is_active = False
        u.save()
        return u


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(max_length=60, required=True)

    # def isValidUsername(self, field_data, all_data):
    #     try:
    #         User.objects.get(username=field_data)
    #     except User.DoesNotExist:
    #         return
    #     raise validators.ValidationError('The username "%s" is already taken.' % field_data)
    def save(self, new_data):
        u = User.objects.create_user(new_data['username'],
                                     new_data['email'],
                                     new_data['password1'])
        u.is_active = False
        u.save()
        return u


class ReagentForm(forms.ModelForm):
    expiry = DateField(input_formats=['%d/%m/%Y', '%Y-%m-%d'])
    class Meta:
        model = Reagent
        fields = ['type', 'lot', 'expiry', 'manufacturer', 'requiresIDcard']

class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=30, required=True)
