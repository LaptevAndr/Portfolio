# MoneyMind - Система управления личными финансами

![Django](https://img.shields.io/badge/Django-4.2-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0-purple)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue)

MoneyMind - это полнофункциональное веб-приложение для управления личными финансами, разработанное на Django. Система предоставляет инструменты для учета доходов и расходов, планирования бюджета, отслеживания финансовых целей и управления кредитами.

## 🚀 Основные функции
- **💰 Управление транзакциями** - учет доходов/расходов с категоризацией, автоматическая дата
- **🎯 Цели накопления** - постановка целей с отслеживанием прогресса и приоритизацией
- **🏦 Управление кредитами** - учет кредитов, графики платежей, процентные ставки
- **📊 Аналитика и отчетность** - визуализация данных, расчет свободных средств, единый формат сумм (0.00 руб.)

## 🛠️ Технологии
**Backend:** Django 4.2, Django ORM, Django Authentication, Django Forms  
**Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript, Plotly  
**База данных:** PostgreSQL/ SQLite

## 📋 Системные требования
- Python 3.8+, Pip, PostgreSQL 13+, Современный браузер

## 🚀 Установка и запуск
```bash
# Клонирование репозитория
git clone https://github.com/LaptevAndr/Portfolio.git
cd Portfolio/MoneyMind

# Настройка виртуального окружения
python -m venv venv

# Активация окружения:
# Linux/MacOS: source venv/bin/activate
# Windows: venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt

# Настройка базы данных
python manage.py makemigrations
python manage.py migrate

# Создание администратора (опционально)
python manage.py createsuperuser

# Запуск сервера разработки
python manage.py runserver