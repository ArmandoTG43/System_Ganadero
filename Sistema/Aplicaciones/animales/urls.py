from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),
    # LOGIN / LOGOUT
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # HOME
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),

    path('AnimalIndex/', views.AnimalIndex, name='AnimalIndex'),
    path('nuevaAnimal/', views.nuevaAnimal, name='nuevaAnimal'),
    path('guardarAnimal/', views.guardarAnimal, name='guardarAnimal'),
    path('editarAnimal/<int:id>/', views.editarAnimal, name='editarAnimal'),
    path('actualizarAnimal/', views.actualizarAnimal, name='actualizarAnimal'),
    path('eliminarAnimal/<int:id>/', views.eliminarAnimal, name='eliminarAnimal'),

    # PDF Animales
    path('generar_pdf_animales/', views.generar_pdf_animales, name='generar_pdf_animales'),

    # EVENTOS
    path('EventoIndex/', views.EventoIndex, name='EventoIndex'),
    path('nuevaEvento/', views.nuevaEvento, name='nuevaEvento'),
    path('guardarEvento/', views.guardarEvento, name='guardarEvento'),
    path('editarEvento/<int:id>/', views.editarEvento, name='editarEvento'),
    path('actualizarEvento/', views.actualizarEvento, name='actualizarEvento'),
    path('eliminarEvento/<int:id>/', views.eliminarEvento, name='eliminarEvento'),

    # PDF Eventos
    path('generar_pdf_eventos/', views.generar_pdf_eventos, name='generar_pdf_eventos'),

    # PRODUCCIÓN
    path('ProduccionIndex/', views.ProduccionIndex, name='ProduccionIndex'),
    path('nuevaProduccion/', views.nuevaProduccion, name='nuevaProduccion'),
    path('guardarProduccion/', views.guardarProduccion, name='guardarProduccion'),
    path('editarProduccion/<int:id>/', views.editarProduccion, name='editarProduccion'),
    path('actualizarProduccion/', views.actualizarProduccion, name='actualizarProduccion'),
    path('eliminarProduccion/<int:id>/', views.eliminarProduccion, name='eliminarProduccion'),

    # PDF Producción
    path('generar_pdf_produccion/', views.generar_pdf_produccion, name='generar_pdf_produccion'),

    path('dashboard/', views.dashboard, name='dashboard'),
    # PERFIL USUARIO
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('cambiar_password/', views.cambiar_password, name='cambiar_password'),

    

]
