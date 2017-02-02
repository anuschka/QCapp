from django import forms
# from django.core import validators
from django.contrib.auth.models import User
from qcapp.models import Reagent
from django.forms import DateField
from django.db.models import Q


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=30, required=True)
    password1 = forms.CharField(max_length=60, required=True)
    password2 = forms.CharField(max_length=60, required=True)

    def save(self, new_data):
        u = User.objects.create_user(new_data['username'],
                                     new_data['email'],
                                     new_data['password1'])
        u.is_active = False
        u.save()
        return u


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(max_length=60, required=True,
                               widget=forms.PasswordInput)

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
    keyword = forms.CharField(max_length=30, required=True, min_length=1)

    def filter_queryset(self, request, queryset):
        q = self.cleaned_data['keyword']
        if q:
            return queryset.filter(
                Q(type__icontains=q) | Q(lot__icontains=q) |
                Q(manufacturer__icontains=q)
                )
        return queryset


class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(
        label=("Email Or Username"), max_length=254)


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2
