from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Animal, Evento, Produccion, Usuario, Perfil
from django.shortcuts import get_object_or_404
from django.contrib.auth import update_session_auth_hash
from .decorators import solo_admin, solo_lectura
from django.db.models import Sum
from datetime import date



@login_required
def cambiar_password(request):
    if request.method == 'POST':
        actual = request.POST.get('password_actual')
        nueva = request.POST.get('password_nueva')
        confirmar = request.POST.get('password_confirmar')

        user = request.user
        # Verificar contraseña actual
        if not user.check_password(actual):
            messages.error(request, 'La contraseña actual es incorrecta')
            return redirect('cambiar_password')

        # Verificar coincidencia
        if nueva != confirmar:
            messages.error(request, 'Las contraseñas nuevas no coinciden')
            return redirect('cambiar_password')

        # Validación básica
        if len(nueva) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres')
            return redirect('cambiar_password')

        # Guardar nueva contraseña
        user.set_password(nueva)
        user.save()

        # Mantener sesión activa
        update_session_auth_hash(request, user)

        messages.success(request, 'Contraseña actualizada correctamente')
        return redirect('perfil')

    return render(request, 'cambiar_password.html')

def registrar_usuario(request):
    admin_existe = Usuario.objects.filter(rol='administrador').exists()

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        rol = request.POST.get('rol')

        if not username or not password or not rol:
            messages.error(request, "Ya no se puede registrar.")
            return redirect('registrar_usuario')

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe.")
            return redirect('registrar_usuario')

        if rol == 'administrador' and admin_existe:
            messages.error(request, "Ya existe un administrador registrado.")
            return redirect('registrar_usuario')

        # 👇 CAMBIO AQUÍ
        usuario = Usuario.objects.create_user(
            username=username,
            password=password,
            rol=rol
        )

        Perfil.objects.create(
            usuario=usuario,
            nombre_completo=username
        )

        messages.success(
            request,
            "Usuario registrado correctamente. Inicie sesión."
        )
        return redirect('login')

    return render(
        request,
        'registrar_usuario.html',
        {'admin_existe': admin_existe}
    )



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Registrar la ventana activa en la sesión
            request.session['window_registered'] = True
            
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'login.html')


def logout_view(request):
    # Limpiar la sesión del localStorage antes de cerrar sesión
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente')
    return redirect('login')

@login_required
def perfil_usuario(request):
    perfil, creado = Perfil.objects.get_or_create(
        usuario=request.user,
        defaults={'nombre_completo': request.user.username}
    )
    return render(request, 'perfil.html', {'perfil': perfil})

@login_required
def editar_perfil(request):
    perfil = request.user.perfil

    if request.method == 'POST':
        perfil.nombre_completo = request.POST['nombre_completo']
        perfil.telefono = request.POST.get('telefono')
        perfil.direccion = request.POST.get('direccion')

        foto = request.FILES.get('foto')
        if foto:
            perfil.foto = foto

        perfil.save()
        messages.success(request, 'Perfil actualizado correctamente')
        return redirect('perfil')

    return render(request, 'editar_perfil.html', {'perfil': perfil})



@login_required
def home(request):
    return render(request, 'home.html')

@login_required
@solo_lectura
def AnimalIndex(request):
    animales = Animal.objects.all()
    return render(request, 'AnimalIndex.html', {'animales': animales})

@login_required
@solo_admin
def nuevaAnimal(request):
    return render(request, 'nuevaAnimal.html')

@login_required
@solo_admin
def guardarAnimal(request):
    tipo = request.POST['tipo']
    sexo = request.POST['sexo']
    fecha_nacimiento = request.POST.get('fecha_nacimiento')
    foto = request.FILES.get('foto')

    Animal.objects.create(tipo=tipo, sexo=sexo, fecha_nacimiento=fecha_nacimiento, foto=foto)
    messages.success(request, 'Animal registrado correctamente')
    return redirect('/AnimalIndex')

@login_required
@solo_admin
def editarAnimal(request, id):
    animal = Animal.objects.get(id=id)
    return render(request, 'editarAnimal.html', {'animal': animal})

@login_required
@solo_admin
def actualizarAnimal(request):
    id = request.POST['id']
    animal = Animal.objects.get(id=id)
    animal.tipo = request.POST['tipo']
    animal.sexo = request.POST['sexo']
    animal.fecha_nacimiento = request.POST.get('fecha_nacimiento')
    foto = request.FILES.get('foto')
    if foto:
        animal.foto = foto
    animal.save()
    messages.success(request, 'Animal actualizado correctamente')
    return redirect('/AnimalIndex')

@login_required
@solo_admin
def eliminarAnimal(request, id):
    Animal.objects.get(id=id).delete()
    messages.success(request, 'Animal eliminado correctamente')
    return redirect('/AnimalIndex')

@login_required
@solo_admin
def generar_pdf_animales(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_animales.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica-Bold", 18)
    p.drawString(150, 750, "REPORTE DE ANIMALES")
    p.line(50, 740, 550, 740)
    p.setFont("Helvetica-Bold", 12)
    y = 720
    p.drawString(50, y, "ID")
    p.drawString(90, y, "Tipo")
    p.drawString(160, y, "Sexo")
    p.drawString(230, y, "Fecha Nac.")
    y -= 20
    p.setFont("Helvetica", 11)
    for a in Animal.objects.all():
        p.drawString(50, y, str(a.id))
        p.drawString(90, y, a.tipo)
        p.drawString(160, y, a.sexo)
        p.drawString(230, y, str(a.fecha_nacimiento) if a.fecha_nacimiento else '')
        y -= 20
        if y < 50:
            p.showPage()
            y = 750
    p.showPage()
    p.save()
    return response

# =============================
# EVENTOS
# =============================
@login_required
@solo_lectura
def EventoIndex(request):
    eventos = Evento.objects.all()
    return render(request, 'EventoIndex.html', {'eventos': eventos})

@login_required
@solo_admin
def nuevaEvento(request):
    animales = Animal.objects.all()
    usuarios = Usuario.objects.all() 
    return render(request, 'nuevaEvento.html', {'animales': animales, 'usuarios': usuarios})

@login_required
@solo_admin
def guardarEvento(request):
    if request.method == "POST":
        try:
            # Obtener datos del formulario
            animal_id = request.POST.get('animal')
            tipo_evento = request.POST.get('tipo_evento')
            fecha_evento = request.POST.get('fecha_evento')
            descripcion = request.POST.get('descripcion', '')
            responsable_id = request.POST.get('responsable')  # id del usuario elegido

            # Validaciones básicas
            if not animal_id or not tipo_evento or not fecha_evento:
                messages.error(request, "Por favor, complete todos los campos obligatorios.")
                return redirect('EventoIndex')

            # Obtener instancias de los modelos
            animal = get_object_or_404(Animal, id=animal_id)

            if responsable_id:
                responsable = get_object_or_404(Usuario, id=responsable_id)
            else:
                # Si no selecciona responsable, asigna el usuario actual
                responsable = request.user

            # Crear el evento
            Evento.objects.create(
                animal=animal,
                tipo_evento=tipo_evento,
                fecha_evento=fecha_evento,
                descripcion=descripcion,
                responsable=responsable
            )

            messages.success(request, "Evento registrado correctamente.")
            return redirect('EventoIndex')

        except Exception as e:
            messages.error(request, f"Ocurrió un error al guardar el evento: {str(e)}")
            return redirect('EventoIndex')

    # Si no es POST, redirige al índice de eventos
    return redirect('EventoIndex')

@login_required
@solo_admin
def editarEvento(request, id):
    evento = Evento.objects.get(id=id)
    return render(request, 'editarEvento.html', {'evento': evento, 'animales': Animal.objects.all()})

@login_required
@solo_admin
def actualizarEvento(request):
    evento = Evento.objects.get(id=request.POST['id'])
    evento.animal = Animal.objects.get(id=request.POST['animal'])
    evento.tipo_evento = request.POST['tipo_evento']
    evento.fecha_evento = request.POST['fecha_evento']
    evento.descripcion = request.POST.get('descripcion','')
    evento.responsable = request.user
    evento.save()
    messages.success(request, 'Evento actualizado correctamente')
    return redirect('/EventoIndex')

@login_required
@solo_admin
def eliminarEvento(request, id):
    Evento.objects.get(id=id).delete()
    messages.success(request, 'Evento eliminado correctamente')
    return redirect('/EventoIndex')

@login_required
@solo_admin
def generar_pdf_eventos(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_eventos.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica-Bold", 18)
    p.drawString(140, 750, "REPORTE DE EVENTOS")
    p.line(50, 740, 550, 740)
    p.setFont("Helvetica-Bold", 12)
    y = 720
    p.drawString(50, y, "ID")
    p.drawString(90, y, "Animal")
    p.drawString(200, y, "Tipo Evento")
    p.drawString(350, y, "Fecha")
    p.drawString(450, y, "Responsable")
    y -= 20
    p.setFont("Helvetica", 11)
    for e in Evento.objects.all():
        p.drawString(50, y, str(e.id))
        p.drawString(90, y, str(e.animal.id))
        p.drawString(200, y, e.tipo_evento)
        p.drawString(350, y, str(e.fecha_evento))
        p.drawString(450, y, e.responsable.username if e.responsable else '')
        y -= 20
        if y < 50:
            p.showPage()
            y = 750
    p.showPage()
    p.save()
    return response

# =============================
# PRODUCCIÓN
# =============================
@login_required
@solo_lectura
def ProduccionIndex(request):
    tipo = request.GET.get('tipo')

    if tipo:
        producciones = Produccion.objects.filter(tipo_producto=tipo)
    else:
        producciones = Produccion.objects.all()

    return render(request, 'ProduccionIndex.html', {
        'producciones': producciones
    })

@login_required
@solo_admin
def nuevaProduccion(request):
    return render(request, 'nuevaProduccion.html', {'animales': Animal.objects.all()})

@login_required
@solo_admin
def guardarProduccion(request):
    animal = Animal.objects.get(id=request.POST['animal'])
    Produccion.objects.create(
        animal=animal,
        tipo_producto=request.POST['tipo_producto'],
        fecha=request.POST['fecha'],
        cantidad=request.POST['cantidad'],
        observaciones=request.POST.get('observaciones','')
    )
    messages.success(request, 'Producción registrada correctamente')
    return redirect('/ProduccionIndex')

@login_required
@solo_admin
def editarProduccion(request, id):
    produccion = Produccion.objects.get(id=id)
    return render(request, 'editarProduccion.html', {'produccion': produccion, 'animales': Animal.objects.all()})

@login_required
@solo_admin
def actualizarProduccion(request):
    produccion = Produccion.objects.get(id=request.POST['id'])
    produccion.animal = Animal.objects.get(id=request.POST['animal'])
    produccion.tipo_producto = request.POST['tipo_producto']
    produccion.fecha = request.POST['fecha']
    produccion.cantidad = request.POST['cantidad']
    produccion.observaciones = request.POST.get('observaciones','')
    produccion.save()
    messages.success(request, 'Producción actualizada correctamente')
    return redirect('/ProduccionIndex')

@login_required
@solo_admin
def eliminarProduccion(request, id):
    Produccion.objects.get(id=id).delete()
    messages.success(request, 'Producción eliminada correctamente')
    return redirect('/ProduccionIndex')

@login_required
@solo_admin
def generar_pdf_produccion(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_produccion.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica-Bold", 18)
    p.drawString(140, 750, "REPORTE DE PRODUCCIÓN")
    p.line(50, 740, 550, 740)
    p.setFont("Helvetica-Bold", 12)
    y = 720
    p.drawString(50, y, "ID")
    p.drawString(90, y, "Animal")
    p.drawString(200, y, "Producto")
    p.drawString(300, y, "Fecha")
    p.drawString(400, y, "Cantidad")
    p.drawString(480, y, "Observaciones")
    y -= 20
    p.setFont("Helvetica", 11)
    for pr in Produccion.objects.all():
        p.drawString(50, y, str(pr.id))
        p.drawString(90, y, str(pr.animal.id))
        p.drawString(200, y, pr.tipo_producto)
        p.drawString(300, y, str(pr.fecha))
        p.drawString(400, y, str(pr.cantidad))
        p.drawString(480, y, pr.observaciones if pr.observaciones else '')
        y -= 20
        if y < 50:
            p.showPage()
            y = 750
    p.showPage()
    p.save()
    return response

@login_required
@solo_lectura
def dashboard(request):
    hoy = date.today()

    context = {
        'total_animales': Animal.objects.count(),
        'total_eventos': Evento.objects.count(),
        'total_produccion': Produccion.objects.aggregate(
            total=Sum('cantidad')
        )['total'] or 0,

        'produccion_mes': Produccion.objects.filter(
            fecha__year=hoy.year,
            fecha__month=hoy.month
        ).aggregate(total=Sum('cantidad'))['total'] or 0,

        'produccion_mensual': (
            Produccion.objects
            .values('fecha__month')
            .annotate(total=Sum('cantidad'))
            .order_by('fecha__month')
        ),

        'produccion_animal': (
            Produccion.objects
            .values('animal__id')
            .annotate(total=Sum('cantidad'))
            .order_by('-total')
        ),
    }
    return render(request, 'dashboard.html', context)
