from django import forms

#SignUp form libraries
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


    
#SignUp form
class SignUpForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Please enter Email address.')
    password = forms.CharField(widget=forms.PasswordInput(), help_text='Please enter Password')
    #telephone number
    last_name = forms.CharField(max_length=10, required=True, help_text='Required. Please enter Telephone number.')

    class Meta:
        model = User
        fields = ('username', 'email', 'last_name', 'password')

    #This function controlled a same username, email and phone register request
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')
        last_name = cleaned_data.get('last_name')

        if email and User.objects.filter(email=email).exists():
            self.add_error('email', 'The email is already taken. Please try another one.')

        if username and User.objects.filter(username=username).exists():
            self.add_error('username', 'The username is already taken. Please try another one.')
        
        if last_name and User.objects.filter(last_name=last_name).exists():
            self.add_error('last_name', 'The phone number is already taken. Please try another one.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            # API anahtarı oluşturma
            Token.objects.create(user=user)
        return user
    

