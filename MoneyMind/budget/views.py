from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction, Category, SavingsGoal, Loan
from .forms import TransactionForm, SavingsGoalForm, LoanForm
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
from decimal import Decimal

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    total_income = sum(t.amount for t in transactions if t.category.type == 'income')
    total_expense = sum(t.amount for t in transactions if t.category.type == 'expense')
    balance = total_income - total_expense
    
    # Получаем цели накопления
    savings_goals = SavingsGoal.objects.filter(user=request.user)
    total_savings_goal = sum(goal.target_amount for goal in savings_goals)
    total_current_savings = sum(goal.current_amount for goal in savings_goals)
    
    # Получаем кредиты
    loans = Loan.objects.filter(user=request.user)
    total_debt = sum(loan.remaining_amount for loan in loans)
    total_monthly_payments = sum(loan.monthly_payment for loan in loans)
    
    # Свободные деньги после обязательных платежей
    free_money_after_expenses = balance - total_monthly_payments if balance else Decimal('0')
    
    # Расчет свободных денег после сбережений (примерный)
    if total_savings_goal > 0:
        monthly_savings_need = (total_savings_goal - total_current_savings) / Decimal('12')
        free_money_after_savings = free_money_after_expenses - monthly_savings_need
    else:
        free_money_after_savings = free_money_after_expenses
    
    # Не допускаем отрицательные значения
    free_money_after_savings = max(free_money_after_savings, Decimal('0'))

    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'savings_goals': savings_goals,
        'loans': loans,
        'total_savings_goal': total_savings_goal,
        'total_current_savings': total_current_savings,
        'total_debt': total_debt,
        'total_monthly_payments': total_monthly_payments,
        'free_money_after_expenses': free_money_after_expenses,
        'free_money_after_savings': free_money_after_savings,
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
    return render(request, 'budget/savings_goals.html', {'goals': goals})

@login_required
def loans_list(request):
    loans = Loan.objects.filter(user=request.user)
    return render(request, 'budget/loans.html', {'loans': loans})

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
    