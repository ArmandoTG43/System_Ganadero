from Aplicaciones.animales.models import Usuario

# Obtener el usuario Armando
try:
    usuario = Usuario.objects.get(username='Armando')
    print(f"Usuario encontrado: {usuario.username}")
    print(f"Rol actual: {usuario.rol}")
    print(f"Es superusuario: {usuario.is_superuser}")
    print(f"Es staff: {usuario.is_staff}")
    
    # Actualizar rol a administrador
    usuario.rol = 'administrador'
    usuario.is_superuser = True
    usuario.is_staff = True
    usuario.save()
    
    print("\n✅ Usuario actualizado:")
    print(f"Nuevo rol: {usuario.rol}")
    print(f"Es superusuario: {usuario.is_superuser}")
    print(f"Es staff: {usuario.is_staff}")
    
except Usuario.DoesNotExist:
    print("❌ Usuario 'Armando' no encontrado")
    
    # Crear nuevo administrador
    admin = Usuario.objects.create_user(
        username='admin',
        email='admin@ganadero.com',
        password='admin123',
        rol='administrador',
        is_superuser=True,
        is_staff=True
    )
    print("✅ Nuevo administrador creado:")
    print(f"Usuario: {admin.username}")
    print(f"Rol: {admin.rol}")
    print(f"Contraseña: admin123")
