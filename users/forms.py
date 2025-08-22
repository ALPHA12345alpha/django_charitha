from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        # Make password fields more user-friendly
        self.fields['password1'].help_text = 'Just pick a password you can remember!'
        self.fields['password2'].help_text = 'Type the same password again'
        self.fields['username'].help_text = 'Pick a cool username!'
        self.fields['email'].help_text = 'We\'ll never spam you, promise!'
        
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 4:
            raise forms.ValidationError('Password must be at least 4 characters long.')
        return password1

class SimpleLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'birth_date', 'avatar', 'theme']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'theme': forms.Select(attrs={'class': 'form-select'}),
        }
