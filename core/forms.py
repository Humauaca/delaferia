from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Nombre de Usuario',
            'class': 'w-full py-4 px-6 rounded-xl',
        }),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'class': 'w-full py-4 px-6 rounded-xl',
        }),
    )

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Nombre de Usuario',
            'class': 'w-full py-4 px-6 rounded-xl',
        }),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email',
            'class': 'w-full py-4 px-6 rounded-xl',
        }),
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'class': 'w-full py-4 px-6 rounded-xl',
        }),
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirmar Contraseña',
            'class': 'w-full py-4 px-6 rounded-xl',
        }),
    )