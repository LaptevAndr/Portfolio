from django.contrib import admin
from .models import Category, Transaction, SavingsGoal, Loan


@admin.register(SavingsGoal)
class SavingsGoalAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'target_amount', 'current_amount', 'progress_percentage', 'deadline']
    list_filter = ['is_completed', 'priority']

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'loan_type', 'total_amount', 'remaining_amount', 'monthly_payment']
    list_filter = ['loan_type']

# Регистрируем модели для отображения в админ-панели
admin.site.register(Category)
admin.site.register(Transaction)