from django import forms
from django.contrib.auth.forms import UserCreationForm

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        data = self.cleaned_data['username']
        return data.strip()  # Remove leading/trailing whitespace

class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password', 'password2']

    def clean_username(self):
        data = self.cleaned_data['username']
        return data.strip() 
