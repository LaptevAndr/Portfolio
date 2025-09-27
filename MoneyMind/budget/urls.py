from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'budget'

urlpatterns = [
    path('', views.home, name='home'),
    
    # Аутентификация
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='budget:home'), name='logout'),
    path('register/', views.register, name='register'),
    
    path('dashboard/', views.transaction_list, name='transaction_list'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('edit/<int:pk>/', views.edit_transaction, name='edit_transaction'), 
    path('delete/<int:pk>/', views.delete_transaction, name='delete_transaction'),
    path('savings/', views.savings_goals, name='savings_goals'),
    path('savings/add/', views.add_savings_goal, name='add_savings_goal'),
    path('loans/', views.loans_list, name='loans_list'),
    path('loans/add/', views.add_loan, name='add_loan'),
    path('savings/edit/<int:pk>/', views.edit_savings_goal, name='edit_savings_goal'),
    path('savings/delete/<int:pk>/', views.delete_savings_goal, name='delete_savings_goal'),
    path('loans/edit/<int:pk>/', views.edit_loan, name='edit_loan'),
    path('loans/delete/<int:pk>/', views.delete_loan, name='delete_loan'),

]