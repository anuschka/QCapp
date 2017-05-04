from django import forms
# from django.core import validators
from django.contrib.auth.models import User
from qcapp.models import Reagent, IdCard, Cell, CellPanel, Essey
from django.forms import DateField


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
    password1 = forms.CharField(label=("New password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=("New password confirmation"),
                                widget=forms.PasswordInput)


class ReagentForm(forms.ModelForm):
    expiry = DateField(input_formats=['%d/%m/%Y', '%Y-%m-%d'])

    class Meta:
        model = Reagent
        fields = ['type', 'lot', 'expiry', 'manufacturer', 'requiresIDcard']


class IdCardForm(forms.ModelForm):
    expiry = DateField(input_formats=['%d/%m/%Y', '%Y-%m-%d'])

    class Meta:
        model = IdCard
        fields = ['type', 'lot', 'expiry', 'manufacturer']


class CellForm(forms.ModelForm):
    expiry = DateField(input_formats=['%d/%m/%Y', '%Y-%m-%d'])

    class Meta:
        model = Cell
        fields = ['number', 'type', 'lot', 'expiry']


class CellPanelForm(forms.ModelForm):
    expiry = DateField(input_formats=['%d/%m/%Y', '%Y-%m-%d'])

    class Meta:
        model = CellPanel
        fields = ['type', 'lot', 'expiry', 'manufacturer', 'sheet']


class EsseyForm(forms.ModelForm):
    expiry = DateField(input_formats=['%d/%m/%Y', '%Y-%m-%d'])

    class Meta:
        model = Essey
        fields = ['type', 'reagent',  'idcard', 'control', 'technician', 'doctor', 'remark', 'consequence']
