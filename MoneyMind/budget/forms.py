from django import forms
from .models import Transaction, SavingsGoal, Loan
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(required=True, max_length=30, label='Имя')
    last_name = forms.CharField(required=True, max_length=30, label='Фамилия')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class CustomLoginForm(AuthenticationForm):
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

class TransactionForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), 
        label='Дата'
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