from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    '''Enhanced user registeration form with additional validation.'''
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 
        'placeholder': 'example@gmail.com'
    }))
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': 'Choose a username'})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Min 8 charecters'}),
        validators=[MinLengthValidator(8)]
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        '''Vallidate email uniqueness.'''
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        
        return email

    def save(self, commit=True):
        '''save user with email.'''
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class CustomAuthenticationForm(AuthenticationForm):
    '''Enhance login form with custom styling.'''

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Username or Email" 
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter your password'
        })
    )

class ProfileForm(forms.ModelForm):
    """Form for editing user profile."""

    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'github_url', 'linkedin_url']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'درباره خودت بنویس...'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/yourusername'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/in/yourusername'
            }),
        }
        labels = {
            'bio': 'بیوگرافی',
            'avatar': 'عکس پروفایل',
            'github_url': 'لینک گیت‌هاب',
            'linkedin_url': 'لینک لینکدین',
        }