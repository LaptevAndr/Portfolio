from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now

# Модель для категорий доходов/расходов (Еда, Транспорт, Зарплата)
class Category(models.Model):
    name = models.CharField(max_length=100)
    # Тип категории: либо доход ('income'), либо расход ('expense')
    TYPE_CHOICES = (
        ('income', 'Доход'),
        ('expense', 'Расход'),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    
    # Поле для отметки кредитных категорий
    is_credit_related = models.BooleanField(default=False, verbose_name='Связано с кредитами')

    # Метод для красивого отображения объекта в админке
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})" 

# Главная модель — транзакция (любой доход или расход)
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Связь с пользователем. Если user удалится, все его транзакции тоже удалятся (CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2) # Сумма. 10 цифр всего
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # Связь с категорией
    date = models.DateField() # Дата операции
    description = models.TextField(blank=True) # Описание, может быть пустым
    
    # Связь с кредитом (если транзакция - платеж по кредиту)
    loan = models.ForeignKey('Loan', on_delete=models.SET_NULL, null=True, blank=True, 
                           verbose_name='Связанный кредит')

    def __str__(self):
        return f"{self.date} - {self.category}: {self.amount}"

# МОДЕЛЬ: Цели накопления
class SavingsGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Название цели')
    target_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Целевая сумма')
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Текущая сумма')
    deadline = models.DateField(verbose_name='Срок достижения', null=True, blank=True)
    priority = models.IntegerField(verbose_name='Приоритет', default=1)
    is_completed = models.BooleanField(default=False, verbose_name='Выполнена')
    
    # Автоматически рассчитываем процент выполнения
    @property
    def progress_percentage(self):
        if self.target_amount > 0:
            return (self.current_amount / self.target_amount) * 100
        return 0
    
    def __str__(self):
        return f"{self.name} - {self.progress_percentage:.1f}%"

# МОДЕЛЬ: Кредиты
class Loan(models.Model):
    LOAN_TYPES = (
        ('credit', 'Потребительский кредит'),
        ('mortgage', 'Ипотека'),
        ('loan', 'Заём'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Название кредита')
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES, verbose_name='Тип кредита')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Общая сумма')
    remaining_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Остаток долга')
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Процентная ставка (%)')
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ежемесячный платеж')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    
    @property
    def months_remaining(self):
        if now().date() < self.end_date:
            delta = relativedelta(self.end_date, now().date())
            return delta.years * 12 + delta.months
        return 0
    
    # Вычисляемое свойство для выплаченной суммы
    @property
    def paid_amount(self):
        return self.total_amount - self.remaining_amount
    
    # Вычисляемое свойство для прогресса выплаты
    @property
    def progress_percentage(self):
        if self.total_amount > 0:
            return (self.paid_amount / self.total_amount) * 100
        return 0
    
    def __str__(self):
        return f"{self.name} - {self.remaining_amount} руб. осталось"