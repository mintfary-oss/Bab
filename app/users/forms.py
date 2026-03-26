from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .models import Profile
User=get_user_model()
class RegistrationForm(UserCreationForm):  # type: ignore[type-arg]
    email=forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control"}))
    expected_due_date=forms.DateField(required=False,widget=forms.DateInput(attrs={"class":"form-control","type":"date"}))
    class Meta:
        model=User
        fields=["username","email","password1","password2","expected_due_date"]
class LoginForm(AuthenticationForm):
    username=forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
class UserProfileForm(forms.ModelForm):  # type: ignore[type-arg]
    class Meta:
        model=User
        fields=["first_name","last_name","avatar","birth_date","expected_due_date","privacy"]
        widgets={"birth_date":forms.DateInput(attrs={"type":"date"}),"expected_due_date":forms.DateInput(attrs={"type":"date"})}
class ProfileDetailForm(forms.ModelForm):  # type: ignore[type-arg]
    class Meta:
        model=Profile
        fields=["bio","location","phone"]
