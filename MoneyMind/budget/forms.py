from django import forms
from .models import Transaction, SavingsGoal, Loan
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re
from datetime import datetime

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@email.com'
        })
    )
    first_name = forms.CharField(
        required=True, 
        max_length=30, 
        label='Имя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваше имя'
        })
    )
    last_name = forms.CharField(
        required=True, 
        max_length=30, 
        label='Фамилия',
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Ваша фамилия'
        })
    )

    password1 = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'autocomplete': 'new-password'
        }),
        help_text=_("Пароль должен содержать минимум 8 символов, включая буквы и цифры."),
    )
    password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтверждение пароля',
            'autocomplete': 'new-password'
        }),
        strip=False,
        help_text=_("Введите тот же пароль, что и выше, для проверки."),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        labels = {
            'username': 'Имя пользователя',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError("Пароль должен содержать минимум 8 символов.")
        if not re.search(r'[A-Za-z]', password1) or not re.search(r'[0-9]', password1):
            raise ValidationError("Пароль должен содержать буквы и цифры.")
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class CustomLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email или логин'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Пароль'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if not username or not password:
            raise ValidationError("Все поля обязательны для заполнения.")
        
        return cleaned_data

class TransactionForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'value': datetime.now().strftime('%Y-%m-%d')
            }
        ), 
        label='Дата',
        initial=datetime.now().date()
    )

    class Meta:
        model = Transaction
        fields = ['amount', 'category', 'date', 'description']

        labels = {
            'amount': 'Сумма',
            'category': 'Категория',
            'description': 'Описание',
        }

        help_texts = {
            'description': 'Необязательное поле',
        }

class SavingsGoalForm(forms.ModelForm):
    class Meta:
        model = SavingsGoal
        fields = ['name', 'target_amount', 'current_amount', 'deadline', 'priority']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'name': 'Название цели',
            'target_amount': 'Целевая сумма',
            'current_amount': 'Текущая сумма',
            'deadline': 'Срок достижения',
            'priority': 'Приоритет (1-10)',
        }

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['name', 'loan_type', 'total_amount', 'remaining_amount', 
                 'interest_rate', 'monthly_payment', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'name': 'Название кредита',
            'loan_type': 'Тип кредита',
            'total_amount': 'Общая сумма',
            'remaining_amount': 'Остаток долга',
            'interest_rate': 'Процентная ставка (%)',
            'monthly_payment': 'Ежемесячный платеж',
            'start_date': 'Дата начала',
            'end_date': 'Дата окончания',
        }