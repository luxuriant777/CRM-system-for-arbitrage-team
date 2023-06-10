from django import forms
from django.contrib.auth.hashers import make_password
from django.forms.widgets import PasswordInput
from user_management.models import CustomUser


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "password", "first_name", "last_name", "email", "position", "image"]
        widgets = {
            'password': PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        image = self.files.get('image')

        if password:
            cleaned_data['password'] = make_password(password)
        if image:
            cleaned_data['image'] = image

        return cleaned_data


class LeadSearchForm(forms.Form):
    search = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by leads"}),
    )
    is_completed = forms.BooleanField(required=False)


class CustomUserSearchForm(forms.Form):
    search = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by users"}),
    )


class PositionSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by positions"}),
    )
