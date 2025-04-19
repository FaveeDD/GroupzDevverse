from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")

    def clean_username(self):
        data = self.cleaned_data['username']
        return data.strip()  # Remove leading/trailing whitespace

    def clean_email(self):
        data = self.cleaned_data['email']
        return data.strip()  # Remove leading/trailing whitespace

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user