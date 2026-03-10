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
            ("farmer", "Farmer"),
            ("labourer", "Labourer"),
            ("student", "Student"),
            ("unemployed", "Unemployed"),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    land_ownership = forms.ChoiceField(
        choices=[("yes", "Yes"), ("no", "No")],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    disability_status = forms.ChoiceField(
        choices=[("yes", "Yes"), ("no", "No")],
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