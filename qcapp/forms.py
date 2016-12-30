from django import forms
# from django.core import validators
from django.contrib.auth.models import User
from qcapp.models import Reagent
from django.forms import DateField
from django.db.models import Q
from django.contrib.auth import authenticate


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

    def form_valid(self, form):
        # username and pass are wrong, return:
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            form.add_error(None, 'Username and/or password are wrong.')
        return self.form_invalid(form)


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
