from django import forms

class AuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
