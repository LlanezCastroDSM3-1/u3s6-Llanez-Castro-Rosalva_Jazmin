# path: función para declarar una ruta URL y a qué vista apunta
from django.urls import path
# views: el módulo con todas las funciones-vista de esta app
from . import views

# urlpatterns: la lista de rutas que Django revisa, en orden, para cada URL
urlpatterns = [
    # '': la página de inicio de la Semana 3 ("Hola desde MySQL"); no la borres
    path('', views.inicio, name='inicio'),
    # /servicios/: la vista de listado
    path('servicios/', views.servicios, name='servicios'),
    # /servicios/nuevo/: formulario en blanco para crear un registro
    path('servicios/nuevo/', views.crear_servicio, name='crear_servicio'),
    # /servicios/<int:pk>/editar/
    path('servicios/<int:pk>/editar/', views.editar_servicio, name='editar_servicio'),
    # /servicios/<int:pk>/eliminar/
    path('servicios/<int:pk>/eliminar/', views.eliminar_servicio, name='eliminar_servicio'),
    # Autenticación y sesiones
    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
]
