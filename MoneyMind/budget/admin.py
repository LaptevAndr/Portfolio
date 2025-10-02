from django.contrib import admin
from .models import Category, Transaction, SavingsGoal, Loan

# Регистрация модели Category с кастомизацией
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'is_credit_related')  # Поля для отображения в списке
    list_filter = ('type', 'is_credit_related')  # Фильтры в правой панели
    search_fields = ('name',)  # Поля для поиска

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'category', 'date', 'loan')
    list_filter = ('category', 'date', 'loan')
    search_fields = ('description', 'category__name')

class SavingsGoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'target_amount', 'current_amount', 'progress_percentage', 'is_completed')
    list_filter = ('is_completed',)

class LoanAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'loan_type', 'total_amount', 'remaining_amount', 'progress_percentage')
    list_filter = ('loan_type',)

# Регистрация моделей в админке
admin.site.register(Category, CategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(SavingsGoal, SavingsGoalAdmin)
admin.site.register(Loan, LoanAdmin)