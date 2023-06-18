from django import forms
from django.contrib.auth.hashers import make_password
from api_users.models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ["username", "password", "first_name", "last_name", "email", "position", "image"]

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            return make_password(password)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = self.cleaned_data.get('password')
        if commit:
            user.save()
        return user


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "email", "position", "image"]


class TeamSearchForm(forms.Form):
    search = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by teams"}),
    )


class ProspectSearchForm(forms.Form):
    search = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by prospects"}),
    )


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
