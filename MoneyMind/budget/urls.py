from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# app_name помогает организовать URL, если несколько приложений имеют view с одинаковыми именами.
app_name = 'budget'

# Список URL-путей для этого приложения.
urlpatterns = [
    # path('URL-адрес/', views.имя_функции, name='имя_для_шаблона'),
    path('', views.home, name='home'),  # главная страница
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.transaction_list, name='transaction_list'),
    path('add/', views.add_transaction, name='add_transaction'),  # Путь /add/ будет вести на страницу добавления.
    path('edit/<int:pk>/', views.edit_transaction, name='edit_transaction'), 
    path('delete/<int:pk>/', views.delete_transaction, name='delete_transaction'),
    path('savings/', views.savings_goals, name='savings_goals'),
    path('savings/add/', views.add_savings_goal, name='add_savings_goal'),
    path('loans/', views.loans_list, name='loans_list'),
    path('loans/add/', views.add_loan, name='add_loan'),
    # Цели накопления - редактирование/удаление
    path('savings/edit/<int:pk>/', views.edit_savings_goal, name='edit_savings_goal'),
    path('savings/delete/<int:pk>/', views.delete_savings_goal, name='delete_savings_goal'),
    # Кредиты - редактирование/удаление
    path('loans/edit/<int:pk>/', views.edit_loan, name='edit_loan'),
    path('loans/delete/<int:pk>/', views.delete_loan, name='delete_loan'),
]