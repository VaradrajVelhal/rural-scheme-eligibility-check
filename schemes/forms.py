from django import forms
from .models import State
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class EligibilityForm(forms.Form):
    income = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    age = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    gender = forms.ChoiceField(
        choices=[
            ("Select Gender","Select"),
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other"),
        ],
    widget=forms.Select(attrs={'class': 'form-select'})
    )

    state = forms.ModelChoiceField(
        queryset=State.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    occupation = forms.ChoiceField(
        choices=[
            ("Select Occupation", "Select Occupation"),
            ("farmer", "Farmer"),
            ("labourer", "Labourer"),
            ("student", "Student"),
            ("unemployed", "Unemployed"),
            ("street_vendor", "Street Vendor"),
            ("other", "Other"),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    land_ownership = forms.ChoiceField(
        choices=[("Select","Select"),("yes", "Yes"), ("no", "No")],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    disability_status = forms.ChoiceField(
        choices=[("Select","Select"),("yes", "Yes"), ("no", "No")],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if password and len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password

    def clean_password2(self):
        password = self.cleaned_data.get("password1")
        confirm_password = self.cleaned_data.get("password2")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return confirm_password