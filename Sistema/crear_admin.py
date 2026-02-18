# Script para crear/actualizar administrador
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

Usuario = get_user_model()

class Command(BaseCommand):
    help = 'Crear o actualizar usuario administrador'

    def handle(self, *args, **options):
        # Buscar si existe usuario Armando
        try:
            usuario = Usuario.objects.get(username='Armando')
            print(f"✅ Usuario '{usuario.username}' encontrado")
            
            # Actualizar a administrador
            usuario.rol = 'administrador'
            usuario.is_superuser = True
            usuario.is_staff = True
            usuario.save()
            
            print(f"🔥 Usuario '{usuario.username}' actualizado a ADMINISTRADOR")
            
        except Usuario.DoesNotExist:
            # Crear nuevo administrador
            usuario = Usuario.objects.create_user(
                username='admin',
                password='admin123',
                rol='administrador',
                is_superuser=True,
                is_staff=True
            )
            print(f"🔥 Nuevo administrador creado: {usuario.username}")
        
        print("\n🎉 Administrador listo!")
        print("📋 Credenciales:")
        if usuario.username == 'Armando':
            print(f"🔹 Usuario: {usuario.username}")
            print("🔹 Contraseña: la que ya tenías")
        else:
            print("🔹 Usuario: admin")
            print("🔹 Contraseña: admin123")
        print("\n✅ Ahora puedes acceder a todo el sistema!")
