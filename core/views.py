# render: junta una plantilla con datos · redirect: manda al navegador a otra URL · get_object_or_404: busca un registro o responde 404
from django.shortcuts import render, redirect, get_object_or_404
# connection: datos de la conexión a la base (lo usa la vista "inicio" de la Semana 3)
from django.db import connection
# login_required: decorador que exige sesión iniciada antes de entrar a la vista
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
# Servicio: el modelo importado desde este mismo directorio
from .models import Servicio
# ServicioForm: el ModelForm
from .forms import ServicioForm


# inicio: la vista de la Semana 3 que muestra a qué base estás conectado (no cambia)
def inicio(request):
    # settings_dict: diccionario con ENGINE, HOST, NAME, etc. de la conexión activa
    info_bd = connection.settings_dict
    # contexto: los datos que la plantilla podrá usar
    contexto = {
        # motor: el tipo de base de datos
        'motor': info_bd['ENGINE'],
        # host: el servidor de la base
        'host': info_bd['HOST'],
    }
    # render: junta inicio.html con el contexto y devuelve la página
    return render(request, 'core/inicio.html', contexto)


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario_nuevo = form.save()
            login(request, usuario_nuevo)
            messages.success(request, f'Cuenta creada. ¡Bienvenido, {usuario_nuevo.username}!')
            return redirect('servicios')
    else:
        form = UserCreationForm()
    return render(request, 'core/registro.html', {'form': form})


def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Sesión iniciada correctamente.')
            return redirect('servicios')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


def cerrar_sesion(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect('login')


# servicios: listado filtrado por el usuario autenticado
@login_required
def servicios(request):
    lista_servicios = Servicio.objects.filter(propietario=request.user)
    return render(request, 'core/servicios.html', {'servicios': lista_servicios})


@login_required
def crear_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            nuevo = form.save(commit=False)
            nuevo.propietario = request.user
            nuevo.save()
            return redirect('servicios')
    else:
        form = ServicioForm()
    return render(request, 'core/servicio_form.html', {'form': form, 'titulo_pagina': 'Nuevo servicio'})


@login_required
def editar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk, propietario=request.user)
    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect('servicios')
    else:
        form = ServicioForm(instance=servicio)
    return render(request, 'core/servicio_form.html', {'form': form, 'titulo_pagina': 'Editar servicio'})


@login_required
def eliminar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk, propietario=request.user)
    if request.method == 'POST':
        servicio.delete()
        return redirect('servicios')
    return render(request, 'core/servicio_confirm_delete.html', {'servicio': servicio})
