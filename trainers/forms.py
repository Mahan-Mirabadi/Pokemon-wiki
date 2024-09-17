from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm  # Assuming trainers.views.py is one level above trainers.forms.py

class TrainerRegisterForm(forms.Form):
    trainer_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'id': 'form3Example3cg'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'id': 'form3Example3cg'}))
    password_1 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'id': 'form3Example3cg'}))
    password_2 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'id': 'form3Example3cg'}))
    
    def clean_user_name(self):
        user = self.cleaned_data['user_name']
        if User.objects.filter(username=user).exists():
            raise forms.ValidationError('Username already exists')
        else:return user
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email already exists')
        else:return email
    def clean_password_2(self):
        pass1=self.cleaned_data['password_1']
        pass2=self.cleaned_data['password_2']
        if pass1!=pass2:
            raise forms.ValidationError('password 1 and 2 are not the same')
        elif len(pass2)<8:
            raise forms.ValidationError('password is shorter than 8 characters')
        elif not any(char.isdigit() for char in pass2) or not any(char.isalpha() for char in pass2):
            raise forms.ValidationError('Password must contain letters and numbers')
        elif not any(i.isupper() for i in pass2):
            raise forms.ValidationError('Password must contain uppercase letter')
        else:return pass1
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class TrainerLoginForm(forms.Form):
    trainer_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'id': 'form3Example3cg'}))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'id': 'form3Example3cg'}))
    def clean(self):
        cleaned_data = super().clean()
        trainer_name = cleaned_data.get('trainer_name')
        password = cleaned_data.get('password')

        try:
            user = User.objects.get(username=trainer_name)
        except User.DoesNotExist:
            raise forms.ValidationError('Trainer name not found.')

        if not authenticate(username=trainer_name, password=password):
            raise forms.ValidationError('Invalid username or password')
        return cleaned_data
#......................................................
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=30,label="Current Password", widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'id': 'form3Example3cg'}))
    new_password1 = forms.CharField(max_length=30,label="New Password", widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'id': 'form3Example3cg'}))
    new_password2 = forms.CharField(max_length=30,label="Confirm New Password", widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'id': 'form3Example3cg'}))
def clean_new_password2(self):
        pass1 = self.cleaned_data.get('new_password1')
        pass2 = self.cleaned_data.get('new_password2')

        if pass1 != pass2:
            raise forms.ValidationError('New passwords do not match.')
        if len(pass2) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        if not any(char.isdigit() for char in pass2) or not any(char.isalpha() for char in pass2):
            raise forms.ValidationError('Password must contain both letters and numbers.')
        if not any(char.isupper() for char in pass2):
            raise forms.ValidationError('Password must contain at least one uppercase letter.')

        return pass2