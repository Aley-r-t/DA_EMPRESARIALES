from django.http import HttpResponse
from django.shortcuts import render
from datetime import date
from django import forms
from django.shortcuts import render, redirect
from decimal import Decimal

def index(request):
    if request.method == 'POST':
        context = {
            'titulo' : 'Formulario',
            'nombre' : request.POST['nombre'],
            'clave'  : request.POST.get('password', 'N/A'),
            'educacion': request.POST.get('educacion'),
            'idiomas': request.POST.getlist('idiomas'),
            'correo': request.POST['email'],
            'website' : request.POST.get('sitioweb', 'N/A'),
        }
        return render(request, 'encuesta/respuesta.html', context)
    else:
        context = {
            'titulo' : 'Formulario',
        }
        return render(request, 'encuesta/index.html')

def enviar(request):
    return render(request, 'encuesta/respuesta.html')

#esto añadi
def calcular_edad(request):
    if request.method == "POST":
        dni = request.POST['dni']
        nombres = request.POST['nombres']
        apellidos = request.POST['apellidos']
        anio = int(request.POST['anio'])
        mes = int(request.POST['mes'])
        dia = int(request.POST['dia'])

        # Calcular edad
        fecha_nacimiento = date(anio, mes, dia)
        hoy = date.today()
        edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

        # Calcular signo zodiacal
        signo_zodiacal = obtener_signo_zodiacal(dia, mes)

        context = {
            'dni': dni,
            'nombres': nombres,
            'apellidos': apellidos,
            'edad': edad,
            'signo_zodiacal': signo_zodiacal
        }

        return render(request, 'encuesta/tarea1.html', context)
    
    return render(request, 'encuesta/tarea1.html')


def obtener_signo_zodiacal(dia, mes):
    if (mes == 3 and dia >= 21) or (mes == 4 and dia <= 19):
        return "Aries"
    elif (mes == 4 and dia >= 20) or (mes == 5 and dia <= 20):
        return "Tauro"
    elif (mes == 5 and dia >= 21) or (mes == 6 and dia <= 20):
        return "Géminis"
    elif (mes == 6 and dia >= 21) or (mes == 7 and dia <= 22):
        return "Cáncer"
    elif (mes == 7 and dia >= 23) or (mes == 8 and dia <= 22):
        return "Leo"
    elif (mes == 8 and dia >= 23) or (mes == 9 and dia <= 22):
        return "Virgo"
    elif (mes == 9 and dia >= 23) or (mes == 10 and dia <= 22):
        return "Libra"
    elif (mes == 10 and dia >= 23) or (mes == 11 and dia <= 21):
        return "Escorpio"
    elif (mes == 11 and dia >= 22) or (mes == 12 and dia <= 21):
        return "Sagitario"
    elif (mes == 12 and dia >= 22) or (mes == 1 and dia <= 19):
        return "Capricornio"
    elif (mes == 1 and dia >= 20) or (mes == 2 and dia <= 18):
        return "Acuario"
    elif (mes == 2 and dia >= 19) or (mes == 3 and dia <= 20):
        return "Piscis"
    
#Parte 2 de Django

# Variables para almacenar los intentos de inicio de sesión
# Variables para almacenar los intentos de inicio de sesión
login_attempts = {}

# Formulario para el inicio de sesión
class LoginForm(forms.Form):
    document_number = forms.CharField(label="Nro Documento", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")

# Formulario para el cálculo de sueldo
class SalaryForm(forms.Form):
    basic_salary = forms.DecimalField(label="Básico", min_value=0)
    years_worked = forms.IntegerField(label="Años de Antigüedad", min_value=0)
    is_married = forms.BooleanField(label="¿Es casado?", required=False)
    children_count = forms.IntegerField(label="Cantidad de Hijos", min_value=0)

def login_view(request):
    global login_attempts

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            document_number = form.cleaned_data['document_number']
            password = form.cleaned_data['password']

            correct_document = "12345678"
            correct_password = "password123"

            if document_number == correct_document and password == correct_password:
                login_attempts[document_number] = 0  # Reiniciar intentos después de un login exitoso
                return redirect('encuesta:calculate_salary')
            else:
                if document_number in login_attempts:
                    login_attempts[document_number] += 1
                else:
                    login_attempts[document_number] = 1

                if login_attempts[document_number] >= 3:
                    return HttpResponse("Acceso bloqueado. Demasiados intentos fallidos.")
                else:
                    return HttpResponse(f"Inicio de sesión incorrecto. Intento {login_attempts[document_number]} de 3.")
    else:
        form = LoginForm()

    return render(request, 'encuesta/login.html', {'form': form})

def calculate_salary(request):
    if request.method == 'POST':
        form = SalaryForm(request.POST)
        if form.is_valid():
            basic_salary = form.cleaned_data['basic_salary']
            years_worked = form.cleaned_data['years_worked']
            is_married = form.cleaned_data['is_married']
            children_count = form.cleaned_data['children_count']

            if children_count <= 7:
                importe_antiguedad = basic_salary * 0.10
            else:
                importe_antiguedad = basic_salary * 0.15

            if is_married:
                importe_estado_civil = basic_salary * 0.02
            else:
                importe_estado_civil = 100

            if children_count <= 4:
                importe_hijos = basic_salary * 0.01 * children_count
            else:
                importe_hijos = 500

            sueldo_total = basic_salary + importe_antiguedad + importe_estado_civil + importe_hijos

            return render(request, 'encuesta/salary_results.html', {
                'basic_salary': basic_salary,
                'years_worked': years_worked,
                'importe_antiguedad': importe_antiguedad,
                'importe_estado_civil': importe_estado_civil,
                'importe_hijos': importe_hijos,
                'sueldo_total': sueldo_total
            })
    else:
        form = SalaryForm()

    return render(request, 'encuesta/tarea1.html', {'form': form})

#parte 3 y final
# Formulario para el cálculo de sueldo
class EmployeeSalaryForm(forms.Form):
    basic_salary = forms.DecimalField(label="Básico", min_value=0, decimal_places=2)
    years_worked = forms.IntegerField(label="Años de Antigüedad", min_value=0)
    is_married = forms.BooleanField(label="¿Es casado?", required=False)
    children_count = forms.IntegerField(label="Cantidad de Hijos", min_value=0)

def calculate_employee_salary(request):
    if request.method == 'POST':
        form = EmployeeSalaryForm(request.POST)
        if form.is_valid():
            basic_salary = form.cleaned_data['basic_salary']
            years_worked = form.cleaned_data['years_worked']
            is_married = form.cleaned_data['is_married']
            children_count = form.cleaned_data['children_count']

            # Convierte los multiplicadores a Decimal
            if children_count <= 7:
                importe_antiguedad = basic_salary * Decimal(0.10)
            else:
                importe_antiguedad = basic_salary * Decimal(0.15)

            if is_married:
                importe_estado_civil = basic_salary * Decimal(0.02)
            else:
                importe_estado_civil = Decimal(100)

            if children_count <= 4:
                importe_hijos = basic_salary * Decimal(0.01) * children_count
            else:
                importe_hijos = Decimal(500)

            sueldo_total = basic_salary + importe_antiguedad + importe_estado_civil + importe_hijos

            return render(request, 'encuesta/salary_results.html', {
                'basic_salary': basic_salary,
                'years_worked': years_worked,
                'importe_antiguedad': importe_antiguedad,
                'importe_estado_civil': importe_estado_civil,
                'importe_hijos': importe_hijos,
                'sueldo_total': sueldo_total
            })
    else:
        form = EmployeeSalaryForm()

    return render(request, 'encuesta/tarea3.html', {'form': form})