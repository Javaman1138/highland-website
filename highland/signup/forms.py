from django import forms
from django.core.validators import EmailValidator
from django.core.validators import ValidationError

class SignUpForm(forms.Form):
    name_errors = {
        'required': 'Name is required',
        'invalid': 'Name is invalid'
    }
    email_errors = {
        'required': 'Email is required',
        'invalid': 'Email is invalid'
    }
    
    name = forms.CharField(max_length=100, required=True, error_messages=name_errors)
    email = forms.EmailField(max_length=100, required=True, error_messages=email_errors)

