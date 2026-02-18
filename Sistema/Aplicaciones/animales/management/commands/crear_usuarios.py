# Script para crear usuarios con roles originales
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.management.base import BaseCommand

Usuario = get_user_model()

class Command(BaseCommand):
    help = 'Crea usuarios con roles originales para el sistema ganadero'

    def handle(self, *args, **options):
        # Eliminar usuarios existentes (excepto superusuarios)
        Usuario.objects.filter(is_superuser=False).delete()
        print("✅ Usuarios anteriores eliminados")

        # Verificar si ya existe un administrador
        admin_existe = Usuario.objects.filter(rol='administrador').exists()
        
        if admin_existe:
            print("⚠️  Ya existe un administrador en el sistema")
            admin = Usuario.objects.get(rol='administrador')
            print(f"🔹 Administrador actual: {admin.username}")
        else:
            # Crear el administrador si no existe
            admin = Usuario.objects.create_user(
                username='admin',
                password='admin123',
                rol='administrador',
                is_superuser=True,
                is_staff=True
            )
            print(f"🔥 Administrador creado: {admin.username}")

        # Crear usuarios de prueba
        usuarios = [
            {
                'username': 'encargado1',
                'password': 'encargado123',
                'rol': 'encargado',
                'is_superuser': False,
                'is_staff': False
            },
            {
                'username': 'revisor1',
                'password': 'revisor123',
                'rol': 'revisor',
                'is_superuser': False,
                'is_staff': False
            }
        ]

        for user_data in usuarios:
            if not Usuario.objects.filter(username=user_data['username']).exists():
                usuario = Usuario.objects.create_user(
                    username=user_data['username'],
                    password=user_data['password'],
                    rol=user_data['rol'],
                    is_superuser=user_data['is_superuser'],
                    is_staff=user_data['is_staff']
                )
                print(f"✅ Usuario creado: {usuario.username} ({usuario.get_rol_display()})")

        print("\n🎉 Sistema de usuarios listo!")
        print("\n📋 Credenciales:")
        print(f"🔹 ADMIN: {admin.username} / admin123")
        print("🔹 ENCARGADO: encargado1 / encargado123")
        print("🔹 REVISOR: revisor1 / revisor123")
        print("\n📝 Permisos:")
        print("🔸 ADMIN: Todos los permisos (solo puede haber UNO)")
        print("🔸 ENCARGADO: Solo lectura")
        print("🔸 REVISOR: Solo lectura")
        print("\n⚠️  IMPORTANTE: Solo puede haber UN administrador")
