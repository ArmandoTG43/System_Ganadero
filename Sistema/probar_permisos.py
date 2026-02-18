# Script para probar usuarios y permisos
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

Usuario = get_user_model()

class Command(BaseCommand):
    help = 'Probar usuarios y permisos'

    def handle(self, *args, **options):
        print("🔍 VERIFICANDO USUARIOS EN EL SISTEMA\n")
        
        usuarios = Usuario.objects.all()
        for usuario in usuarios:
            print(f"👤 Usuario: {usuario.username}")
            print(f"   Rol: {usuario.get_rol_display()}")
            print(f"   Staff: {usuario.is_staff}")
            print(f"   Superuser: {usuario.is_superuser}")
            print(f"   Activo: {usuario.is_active}")
            print()
        
        print("📋 PERMISOS POR ROL:")
        print("🔴 ADMINISTRADOR:")
        print("   ✅ Puede VER: Animales, Eventos, Producción, Dashboard")
        print("   ✅ Puede CREAR: Animales, Eventos, Producción")
        print("   ✅ Puede EDITAR: Animales, Eventos, Producción")
        print("   ✅ Puede ELIMINAR: Animales, Eventos, Producción")
        print("   ✅ Puede EXPORTAR: PDFs")
        print()
        print("🟡 ENCARGADO:")
        print("   ✅ Puede VER: Animales, Eventos, Producción, Dashboard")
        print("   ❌ Puede CREAR: NADA")
        print("   ❌ Puede EDITAR: NADA")
        print("   ❌ Puede ELIMINAR: NADA")
        print("   ❌ Puede EXPORTAR: NADA")
        print()
        print("🟠 REVISOR:")
        print("   ✅ Puede VER: Animales, Eventos, Producción, Dashboard")
        print("   ❌ Puede CREAR: NADA")
        print("   ❌ Puede EDITAR: NADA")
        print("   ❌ Puede ELIMINAR: NADA")
        print("   ❌ Puede EXPORTAR: NADA")
        print()
        print("🎯 LISTO PARA PROBAR!")
        print("📌 Inicia sesión con cada usuario para verificar permisos")
