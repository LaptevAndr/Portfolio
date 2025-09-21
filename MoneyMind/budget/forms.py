from django import forms
from .models import Transaction, SavingsGoal, Loan


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