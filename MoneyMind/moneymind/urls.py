from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from budget import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='index'),
    
    # Аутентификация
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    path('budget/', include('budget.urls')),
]