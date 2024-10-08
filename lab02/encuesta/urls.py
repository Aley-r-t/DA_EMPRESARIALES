"""
URL configuration for encuesta project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path

app_name = 'encuesta'

urlpatterns = [
    path('', views.index, name='index'),
    path('enviar', views.enviar, name='enviar'),
    path('calcular', views.calcular_edad, name='calcular_edad'),

    path('login/', views.login_view, name='login'),  # URL para el login
    path('calculate-salary/', views.calculate_salary, name='calculate_salary'),
    path('calculate-employee-salary/', views.calculate_employee_salary, name='calculate_employee_salary'), 
]
