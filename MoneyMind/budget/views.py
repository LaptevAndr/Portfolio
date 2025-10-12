from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction, Category, SavingsGoal, Loan
from .forms import TransactionForm, SavingsGoalForm, LoanForm
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
from decimal import Decimal
from django.db.models import Sum, Q
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CustomUserCreationForm 
from datetime import datetime, timedelta
from django.db import models
from django.db.models import Sum
from budget.models import Category, Transaction, Loan, SavingsGoal
from django.utils import timezone
import random

def home(request):
    """Главная страница приложения"""
    return render(request, 'budget/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('budget:transaction_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def create_demo_data(request):
    """
    Создание демонстрационных данных для тестирования интерфейса
    """
    user = request.user
    
    try:
        # Удаление старых демо-данных этого пользователя
        Transaction.objects.filter(user=user, description__contains='[Демо]').delete()
        Loan.objects.filter(user=user, name__contains='[Демо]').delete()
        SavingsGoal.objects.filter(user=user, name__contains='[Демо]').delete()
        
        income_categories = [
            ('Зарплата', 'income'),
            ('Фриланс', 'income'),
            ('Инвестиции', 'income'),
            ('Подарки', 'income'),
        ]
        
        expense_categories = [
            ('Продукты', 'expense'),
            ('Транспорт', 'expense'),
            ('Коммунальные услуги', 'expense'),
            ('Развлечения', 'expense'),
            ('Одежда', 'expense'),
            ('Здоровье', 'expense'),
        ]
        
        categories_map = {}
        
        for name, cat_type in income_categories + expense_categories:
            category, created = Category.objects.get_or_create(
                name=name,
                type=cat_type,
                defaults={'user': user}
            )
            categories_map[name] = category
        
        # Создание демо-транзакции (доходы)
        income_transactions = [
            (categories_map['Зарплата'], 120000, 'Зарплата за октябрь'),
            (categories_map['Фриланс'], 35000, 'Проект для клиента'),
            (categories_map['Инвестиции'], 15000, 'Дивиденды по акциям'),
        ]
        
        for category, amount, description in income_transactions:
            Transaction.objects.create(
                user=user,
                category=category,
                amount=amount,
                date=timezone.now().date() - timedelta(days=10),
                description=f'[Демо] {description}'
            )
        
        # Создание демо-транзакции (расходы)
        expense_transactions = [
            (categories_map['Продукты'], 25000, 'Продукты на неделю'),
            (categories_map['Транспорт'], 8000, 'Бензин и проездной'),
            (categories_map['Коммунальные услуги'], 12000, 'Квартплата'),
            (categories_map['Развлечения'], 15000, 'Рестораны и кино'),
            (categories_map['Одежда'], 18000, 'Новая куртка'),
            (categories_map['Здоровье'], 5000, 'Визит к врачу'),
        ]
        
        for category, amount, description in expense_transactions:
            Transaction.objects.create(
                user=user,
                category=category,
                amount=amount,
                date=timezone.now().date() - timedelta(days=random.randint(1, 30)),
                description=f'[Демо] {description}'
            )
        
        # Создание демо-кредиты
        demo_loans = [
            {
                'name': '[Демо] Ипотека',
                'loan_type': 'mortgage',
                'total_amount': 3500000,
                'remaining_amount': 3200000,
                'monthly_payment': 45000,
                'interest_rate': 7.5,
                'start_date': timezone.now().date() - timedelta(days=400),
                'end_date': timezone.now().date() + timedelta(days=3000)
            },
            {
                'name': '[Демо] Автокредит', 
                'loan_type': 'consumer',
                'total_amount': 900000,
                'remaining_amount': 420000,
                'monthly_payment': 28000,
                'interest_rate': 11.9,
                'start_date': timezone.now().date() - timedelta(days=200),
                'end_date': timezone.now().date() + timedelta(days=600)
            },
            {
                'name': '[Демо] Потребительский кредит',
                'loan_type': 'consumer', 
                'total_amount': 300000,
                'remaining_amount': 120000,
                'monthly_payment': 15000,
                'interest_rate': 15.2,
                'start_date': timezone.now().date() - timedelta(days=100),
                'end_date': timezone.now().date() + timedelta(days=200)
            }
        ]
        
        created_loans = []
        for loan_data in demo_loans:
            loan = Loan.objects.create(user=user, **loan_data)
            created_loans.append(loan)
        
        # Создание демо-цели накопления
        SavingsGoal.objects.create(
            user=user,
            name='[Демо] Отпуск в Турции',
            target_amount=150000,
            current_amount=75000,
            deadline=timezone.now().date() + timedelta(days=180),
            priority=8
        )
        
        SavingsGoal.objects.create(
            user=user,
            name='[Демо] Новый ноутбук',
            target_amount=80000,
            current_amount=45000,
            deadline=timezone.now().date() + timedelta(days=90),
            priority=6
        )
        
        SavingsGoal.objects.create(
            user=user,
            name='[Демо] Резервный фонд',
            target_amount=300000,
            current_amount=120000,
            deadline=timezone.now().date() + timedelta(days=365),
            priority=10
        )
        
        # СОЗДАНИЕ ТРАНЗАКЦИЙ ПО КРЕДИТАМ ДЛЯ ГРАФИКА
        credit_category, _ = Category.objects.get_or_create(
            name='Кредитные платежи',
            type='expense',
            defaults={'user': user, 'is_credit_related': True}
        )
        
        for loan in created_loans:
            # Создание несколькИХ платежей по каждому кредиту
            for i in range(3):
                Transaction.objects.create(
                    user=user,
                    category=credit_category,
                    amount=loan.monthly_payment,
                    date=timezone.now().date() - timedelta(days=30 * (i + 1)),
                    description=f'[Демо] Платеж по {loan.name}',
                    loan=loan
                )
        
        messages.success(request, '🎉 Демонстрационные данные успешно созданы! Теперь вы можете протестировать все функции приложения.')
        
    except Exception as e:
        messages.error(request, f'❌ Ошибка при создании демо-данных: {str(e)}')
    
    return redirect('budget:transaction_list')

@login_required
def clear_demo_data(request):
    """
    Очистка демонстрационных данных
    """
    user = request.user
    
    try:
        # Получаем количество объектов ДО удаления
        transactions_count = Transaction.objects.filter(
            user=user, 
            description__contains='[Демо]'
        ).count()
        
        loans_count = Loan.objects.filter(
            user=user,
            name__contains='[Демо]'
        ).count()
        
        goals_count = SavingsGoal.objects.filter(
            user=user,
            name__contains='[Демо]'
        ).count()
        
        # Удаляем демо-данные
        Transaction.objects.filter(
            user=user, 
            description__contains='[Демо]'
        ).delete()
        
        Loan.objects.filter(
            user=user,
            name__contains='[Демо]'
        ).delete()
        
        SavingsGoal.objects.filter(
            user=user,
            name__contains='[Демо]'
        ).delete()
        
        messages.info(request, f'✅ Демонстрационные данные очищены: {transactions_count} транзакций, {loans_count} кредитов, {goals_count} целей')
        
    except Exception as e:
        messages.error(request, f'❌ Ошибка при очистке данных: {str(e)}')
    
    return redirect('budget:transaction_list')

def user_has_demo_data(user):
    """Проверяет, есть ли у пользователя демо-данные"""
    return (
        Transaction.objects.filter(user=user, description__contains='[Демо]').exists() or
        Loan.objects.filter(user=user, name__contains='[Демо]').exists() or
        SavingsGoal.objects.filter(user=user, name__contains='[Демо]').exists()
    )

@login_required
def transaction_list(request):
    # Фильтрация за последние 30 дней для статистики
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    
    # Все транзакции для истории
    all_transactions = Transaction.objects.filter(user=request.user).select_related('category', 'loan').order_by('-date')
    
    # Транзакции за последние 30 дней для статистики
    recent_transactions = all_transactions.filter(date__gte=thirty_days_ago)
    
    # Базовая статистика за 30 дней
    income_agg = recent_transactions.filter(category__type='income').aggregate(total=Sum('amount'))
    expense_agg = recent_transactions.filter(category__type='expense').aggregate(total=Sum('amount'))
    
    total_income = income_agg['total'] or Decimal('0')
    total_expense = expense_agg['total'] or Decimal('0')
    balance = total_income - total_expense

    # Форматируем числа
    total_income = total_income.quantize(Decimal('0.01'))
    total_expense = total_expense.quantize(Decimal('0.01'))
    balance = balance.quantize(Decimal('0.01'))

    # Данные для основной финансовой диаграммы (доходы/расходы)
    main_chart_data = None
    if total_income > 0 or total_expense > 0:
        main_chart_data = {
            'labels': ['Доходы', 'Расходы'],
            'values': [float(total_income), float(total_expense)],
            'colors': ['#28a745', '#dc3545']
        }

    # Диаграмма расходов по категориям за 30 дней
    expense_categories_data = None
    expense_by_category = recent_transactions.filter(
        category__type='expense'
    ).values('category__name').annotate(total=Sum('amount')).order_by('-total')
    
    if expense_by_category:
        expense_categories_data = {
            'labels': [item['category__name'] for item in expense_by_category],
            'values': [float(item['total']) for item in expense_by_category],
            'colors': ['#dc3545', '#e74c3c', '#c0392b', '#ff6b6b', '#ee5a24']
        }

    # ДИАГРАММА КРЕДИТНЫХ ПЛАТЕЖЕЙ
    credit_payments_data = None
    user_loans = Loan.objects.filter(user=request.user)
    
    if user_loans.exists():

        loan_names = []
        monthly_payments = []
        colors = ['#8e44ad', '#9b59b6', '#3498db', '#2980b9', '#1abc9c']
        
        for i, loan in enumerate(user_loans):
            loan_names.append(loan.name.replace('[Демо] ', ''))
            monthly_payments.append(float(loan.monthly_payment))
        
        credit_payments_data = {
            'labels': loan_names,
            'values': monthly_payments,
            'colors': colors[:len(loan_names)]
        }
        
    # Диаграмма накоплений
    savings_chart_data = None
    savings_goals = SavingsGoal.objects.filter(user=request.user)
    if savings_goals.exists():
        savings_chart_data = {
            'labels': [goal.name for goal in savings_goals],
            'current_values': [float(goal.current_amount) for goal in savings_goals],
            'target_values': [float(goal.target_amount) for goal in savings_goals],
            'progress': [float(goal.progress_percentage) for goal in savings_goals],
            'colors': ['#27ae60', '#2ecc71', '#1abc9c', '#16a085']
        }

    # Диаграмма кредитов
    loans_chart_data = None
    loans = Loan.objects.filter(user=request.user)
    if loans.exists():
        loans_chart_data = {
            'labels': [loan.name for loan in loans],
            'paid_values': [float(loan.paid_amount) for loan in loans],
            'remaining_values': [float(loan.remaining_amount) for loan in loans],
            'progress': [float(loan.progress_percentage) for loan in loans],
            'colors': ['#e74c3c', '#c0392b', '#d35400', '#e67e22']
        }

    # Общая статистика
    total_savings_goal = sum(goal.target_amount for goal in savings_goals) or Decimal('0')
    total_current_savings = sum(goal.current_amount for goal in savings_goals) or Decimal('0')
    
    total_debt = sum(loan.remaining_amount for loan in loans) or Decimal('0')
    total_monthly_payments = sum(loan.monthly_payment for loan in loans) or Decimal('0')
    
    # Свободные деньги
    free_money_after_expenses = balance - total_monthly_payments
    free_money_after_savings = free_money_after_expenses
    
    if total_savings_goal > 0 and total_savings_goal > total_current_savings:
        monthly_savings_need = (total_savings_goal - total_current_savings) / Decimal('12')
        free_money_after_savings = free_money_after_expenses - monthly_savings_need
    
    free_money_after_savings = max(free_money_after_savings, Decimal('0'))
    free_money_after_expenses = max(free_money_after_expenses, Decimal('0'))

    context = {
        'transactions': all_transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'main_chart_data': main_chart_data,
        'expense_categories_data': expense_categories_data,
        'credit_payments_data': credit_payments_data,
        'savings_chart_data': savings_chart_data,
        'loans_chart_data': loans_chart_data,
        'savings_goals': savings_goals,
        'loans': loans,
        'total_savings_goal': total_savings_goal,
        'total_current_savings': total_current_savings,
        'total_debt': total_debt,
        'total_monthly_payments': total_monthly_payments,
        'free_money_after_expenses': free_money_after_expenses,
        'free_money_after_savings': free_money_after_savings,
        'period_days': 30,  # Показываем период в шаблоне
        'user_demo_data_exists': user_has_demo_data(request.user),
    }
    return render(request, 'budget/transaction_list.html', context)

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            new_transaction = form.save(commit=False)
            new_transaction.user = request.user
            new_transaction.save()
            return redirect('budget:transaction_list')
    else:
        form = TransactionForm()

    context = {'form': form}
    return render(request, 'budget/transaction_form.html', context)

@login_required
def savings_goals(request):
    goals = SavingsGoal.objects.filter(user=request.user)
    total_savings_goal = goals.aggregate(total=Sum('target_amount'))['total'] or 0
    total_current_savings = goals.aggregate(total=Sum('current_amount'))['total'] or 0
    
    remaining_amount = total_savings_goal - total_current_savings
    
    context = {
        'goals': goals,
        'total_savings_goal': total_savings_goal,
        'total_current_savings': total_current_savings,
        'remaining_amount': remaining_amount,
    }
    return render(request, 'budget/savings_goals.html', context)

def calculate_free_money_after_expenses(user):
    try:
        # Сумма всех доходов
        total_income = Transaction.objects.filter(
            user=user, 
            category__type='income'
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Сумма расходов (исключая кредитные платежи, если они есть в транзакциях)
        total_expenses = Transaction.objects.filter(
            user=user, 
            category__type='expense'
        ).exclude(
            # Исключаем категории, связанные с кредитами
            category__name__icontains='кредит'
        ).exclude(
            category__name__icontains='займ'
        ).exclude(
            category__name__icontains='loan'
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Ежемесячные платежи по кредитам из модели Loan
        total_loan_payments = Loan.objects.filter(
            user=user
        ).aggregate(Sum('monthly_payment'))['monthly_payment__sum'] or 0
        
        # Свободные средства = доходы - расходы - кредитные платежи
        free_money = total_income - total_expenses - total_loan_payments
        return max(free_money, 0)  # Не допускаем отрицательные значения
        
    except Exception as e:
        print(f"Ошибка расчета свободных средств: {e}")
        return 0
    
@login_required
def loans_list(request):
    loans = Loan.objects.filter(user=request.user)
    
    # Вычисляем общую статистику
    total_debt = sum(loan.remaining_amount for loan in loans)
    total_monthly_payments = sum(loan.monthly_payment for loan in loans)
    
    # Используем функцию расчета свободных средств
    free_money_after_expenses = calculate_free_money_after_expenses(request.user)
    
    context = {
        'loans': loans,
        'total_debt': total_debt,
        'total_monthly_payments': total_monthly_payments,
        'free_money_after_expenses': free_money_after_expenses,
    }
    return render(request, 'budget/loans.html', context)

@login_required
def add_savings_goal(request):
    if request.method == 'POST':
        form = SavingsGoalForm(request.POST)
        if form.is_valid():
            new_goal = form.save(commit=False)
            new_goal.user = request.user
            new_goal.save()
            return redirect('budget:savings_goals')
    else:
        form = SavingsGoalForm()

    context = {'form': form}
    return render(request, 'budget/savings_goal_form.html', context)

@login_required
def add_loan(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            new_loan = form.save(commit=False)
            new_loan.user = request.user
            new_loan.save()
            return redirect('budget:loans_list')
    else:
        form = LoanForm()

    context = {'form': form}
    return render(request, 'budget/loan_form.html', context)

@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, id=pk, user=request.user)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('budget:transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    
    context = {'form': form, 'transaction': transaction}
    return render(request, 'budget/transaction_form.html', context)

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, id=pk, user=request.user)
    
    if request.method == 'POST':
        transaction.delete()
        return redirect('budget:transaction_list')
    else:
        return render(request, 'budget/transaction_confirm_delete.html', {'transaction': transaction})

@login_required
def edit_savings_goal(request, pk):
    goal = get_object_or_404(SavingsGoal, id=pk, user=request.user)
    
    if request.method == 'POST':
        form = SavingsGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('budget:savings_goals')
    else:
        form = SavingsGoalForm(instance=goal)
    
    context = {'form': form, 'goal': goal}
    return render(request, 'budget/savings_goal_form.html', context)

@login_required
def delete_savings_goal(request, pk):
    goal = get_object_or_404(SavingsGoal, id=pk, user=request.user)
    
    if request.method == 'POST':
        goal.delete()
        return redirect('budget:savings_goals')
    else:
        return render(request, 'budget/savings_goal_confirm_delete.html', {'goal': goal})

@login_required
def edit_loan(request, pk):
    loan = get_object_or_404(Loan, id=pk, user=request.user)
    
    if request.method == 'POST':
        form = LoanForm(request.POST, instance=loan)
        if form.is_valid():
            form.save()
            return redirect('budget:loans_list')
    else:
        form = LoanForm(instance=loan)
    
    context = {'form': form, 'loan': loan}
    return render(request, 'budget/loan_form.html', context)

@login_required
def delete_loan(request, pk):
    loan = get_object_or_404(Loan, id=pk, user=request.user)
    
    if request.method == 'POST':
        loan.delete()
        return redirect('budget:loans_list')
    else:
        return render(request, 'budget/loan_confirm_delete.html', {'loan': loan})
    
@login_required
def add_balance(request):
    """
    Создание начального баланса через специальную транзакцию
    """
    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description', 'Начальный баланс')
        
        if amount:
            try:
                # Создаем категорию для баланса или находим существующую
                balance_category, created = Category.objects.get_or_create(
                    name='Начальный баланс',
                    user=request.user,  # Добавляем пользователя
                    defaults={
                        'type': 'income',
                        'is_credit_related': False
                    }
                )
                
                # Создаем транзакцию баланса
                balance_transaction = Transaction.objects.create(
                    user=request.user,
                    amount=amount,
                    category=balance_category,
                    date=timezone.now().date(),
                    description=description
                )
                
                messages.success(request, f'Начальный баланс {amount} ₽ успешно установлен!')
                return redirect('budget:transaction_list')
                
            except Exception as e:
                messages.error(request, f'Ошибка при создании баланса: {str(e)}')
        else:
            messages.error(request, 'Пожалуйста, укажите сумму баланса')
    
    return render(request, 'budget/balance_form.html')