from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from django.core.exceptions import ValidationError

###SIGN-UP-FORM###
class SignUpForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Gerekli. E-posta adresinizi girin.')
    phone = forms.CharField(max_length=10, required=True, help_text='Gerekli. Telefon numaranızı girin.')
    password = forms.CharField(widget=forms.PasswordInput(), help_text='Parolanızı girin.')

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password')

    #This function controlled a same username and email register request
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')

        if email and User.objects.filter(email=email).exists():
            self.add_error('email', 'The email is already taken. Please try another one.')

        if username and User.objects.filter(username=username).exists():
            self.add_error('username', 'The username is already taken. Please try another one.')

        return cleaned_data

    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.phone = self.cleaned_data['phone']

        if commit:
            user.save()
            # API anahtarı oluşturma
            Token.objects.create(user=user)
        return user
