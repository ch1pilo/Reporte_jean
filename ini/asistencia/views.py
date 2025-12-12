from sqlite3 import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from asistencia import models
from django.contrib.auth.models import User

def eliminar_persona(request, id):
    
    usuario = User.objects.get(id=id)
    usuario_activo = models.Inscripcion.objects.filter(usuario = usuario) 
    if not usuario_activo.exists():
        
        u = models.datos_personales.objects.filter(id_user=usuario).delete()
        us = User.objects.filter(id=id).delete()
        print('usuario eliminado')
        return redirect('persona')

    else:
        print('el usuario no se puede eliminar porque tiene registros')
        return redirect('persona')


def eliminar_programa(request, id):
    
    usuario_activo = models.Inscripcion.objects.filter(programa = id) 
    if not usuario_activo.exists():
        usuario_activo.delete()
        print('programa eliminado')
        return redirect('editar_programa')

    else:
        print('el programa no se puede eliminar porque tiene registros')
        return redirect('programa')

def editar_programa(request, id):
    if request.method == 'POST':

        nombre = request.POST.get('nombre')
        codigo = request.POST.get('codigo')
        estatus = request.POST.get('estatus') 

        models.Programa.objects.filter(id=id).update(
            nombre = nombre,
            codigo = codigo,
            estatus = estatus 
        )
        print('programa editado correctamente ')

        return redirect('detalle_programas', id)
    else:
        programa = models.Programa.objects.get(id=id)
        return render (request, 'editar_programa.html', {'programa':programa})

def editar_modulo(request, id):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        fecha = request.POST.get('fecha')
        estatus = request.POST.get('estatus')

        models.Modulo.objects.filter(id=id).update(
            nombre = nombre,
            fecha = fecha,
            estatus = estatus,
        )
        return redirect('programa')
    else:
        modulo = models.Modulo.objects.get(id = id)
        print(modulo.fecha) 
        return render(request, 'editar_modulo.html', {'modulo':modulo})

def eliminar_modulo(request, id):
    usuario_activo = models.Asistencia.objects.filter(modulo = id) 
    for i in usuario_activo:
        print (f'esto es {i.modulo.nombre}')
    programa = models.Modulo.objects.get(id=id)
    modulos = models.Modulo.objects.filter(id=id)
    print(programa.programa.id)
    if not usuario_activo.exists():
        modulos.delete()
        print('modulo eliminado')
        return redirect('detalle_programas', programa.programa.id)

    else:
        print('el modulo no se puede eliminar porque tiene registros')
        return redirect('programa')

def logout_views(request):
    logout(request)
    return redirect('index')

def logueado(request):
    if request.method == 'POST':
        try:
            user = request.POST.get('nombre')
            contrasena = request.POST.get('pasword')

            print(f'{user} {contrasena}')

            usuario = authenticate(request, username=user, password=contrasena)

            if usuario is not None:
                login(request, usuario)
                print('logueado con éxito')

                # ✅ Captura el parámetro next
                persona = models.datos_personales.objects.all() 
                personas_max = len(persona)
                programa = models.Programa.objects.all()
                programa_max = len(programa)
                next_url = request.GET.get('next') or request.POST.get('next') or 'dashboard'
                if next_url == 'dashboard':
                    print(f' personas maximas {personas_max}')
                    return render(request, 'dashboard.html', {'personas':personas_max,
                                                              'programa_max': programa_max})
                return redirect(next_url)
            else:
                print('error al loguear')
                return redirect('index')
        except Exception as e:
            print(f'el error es {e}')
            return redirect('index')
    else:
        return redirect('index')
    
def index(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    persona = models.datos_personales.objects.all() 
    personas_max = len(persona)
    programa = models.Programa.objects.filter(estatus=True)
    programa_max = len(programa)
    return render(request, 'dashboard.html', {'personas':personas_max,
                                              'programa_max': programa_max})

def crear_programa(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        codigo = request.POST.get('codigo')

        models.Programa(
            nombre = nombre,
            codigo = codigo,
        ).save()

        print('programa guardado')
        return redirect('crear_programa')
    else:
        return render(request, 'crear_programa.html')

def programa(request):
    programas = models.Programa.objects.all()
    return render(request, 'modulo_programa.html', {'programas' : programas})



def detalle_programas (request, id):
    programa = models.Programa.objects.get(id=id)
    modulos_prograsma = models.Modulo.objects.filter(programa = id)
    return render (request, 'detalle_programas.html', {'programa':programa,
                                                       'modulos':modulos_prograsma})

def crear_modulo(request, id):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        fecha = request.POST.get('fecha')
        prograam = models.Programa.objects.get(id=id)
        models.Modulo(
            programa = prograam,
            nombre = nombre,
            fecha = fecha,
        ).save()
        print('modulo guardado correctamente')
        return redirect('detalle_programas', id)
    else:
        programa_sujeto = models.Programa.objects.get(id=id)
        print(programa_sujeto.nombre, programa_sujeto.id)
        return render(request, 'nuevo_modulo.html', {'programa_id':programa_sujeto})

def inscripcion(request): 
    inscripciones = models.Inscripcion.objects.filter()
    for i in inscripciones:
        print(i.usuario.datos_personales.nombre) 
    return render(request, 'modulo_inscripcion.html', {'inscripciones': inscripciones})

def vista_seleccionar_programa(request):
    programas = models.Programa.objects.all()
    
    return render(request, 'inscribir.html', {'programas': programas})

def asistencia(request):
    programas = models.Programa.objects.all()
    return render(request, 'asistencia.html', {'programas': programas})

# views.py (Función registrar_asistencia)

def registrar_asistencia(request, id):
    modulo = get_object_or_404(models.Modulo, id=id)
    
    # 1. Obtenemos todos los inscritos en el programa del módulo
    inscritos = models.Inscripcion.objects.filter(programa=modulo.programa)
    
    lista_asistencia = []
    
    # 2. Iteramos sobre los inscritos para determinar su estado
    for inscripcion in inscritos:
        
        # Intentamos obtener la asistencia previamente guardada para este estudiante Y este módulo
        try:
            asistencia_guardada = models.Asistencia.objects.get(
                inscripcion=inscripcion, 
                modulo=modulo
            )
            # Si existe, usamos el valor guardado
            asistio_estado = asistencia_guardada.asistio
            
        except models.Asistencia.DoesNotExist:
            # Si NO existe, asumimos el estado por defecto: TRUE (Asistió)
            asistio_estado = True 
            
        lista_asistencia.append({
            'inscripcion_id': inscripcion.id,
            # Ahora podemos acceder al nombre de la persona gracias al OneToOneField corregido:
            'nombre_completo': inscripcion.usuario.datos_personales.nombre, 
            'cedula': inscripcion.usuario.datos_personales.cedula,
            'asistio': asistio_estado, # True o False
        })
    
    context = {
        'modulo': modulo,
        'programa': modulo.programa,
        'lista_asistencia': lista_asistencia # Enviamos la lista procesada
    }
    return render(request, 'registrar_asistencia.html', context)

# 3. Guardar la Asistencia (Lógica del botón Guardar)
def guardar_asistencia(request, id):
    modulo = get_object_or_404(models.Modulo, id=id)
    
    if request.method == 'POST':
        inscritos = models.Inscripcion.objects.filter(programa=modulo.programa)
        
        for inscripcion in inscritos:
            # El checkbox se llama "asistencia_ID"
            checkbox_name = f'asistencia_{inscripcion.id}'
            # Si está marcado devuelve 'on', si no devuelve None
            presente = request.POST.get(checkbox_name) == 'on'
            
            # Guardamos o actualizamos la asistencia
            models.Asistencia.objects.update_or_create(
                inscripcion=inscripcion,
                modulo=modulo,
                defaults={'asistio': presente} 
            )
            
        print("Asistencias guardadas")
        return redirect('asistencia') # Volvemos al panel principal

    return redirect('asistencia')

def inscribir_programa(request, id):
    programa_seleccionado = get_object_or_404(models.Programa, id=id)

    if request.method == 'POST':
        try:
            usuario_id = request.POST.get('usuario_id')
            
            usuario_obj = User.objects.get(id=usuario_id)
            
            nueva_inscripcion = models.Inscripcion(
                programa=programa_seleccionado,
                usuario=usuario_obj
            )
            nueva_inscripcion.save()
            
            print(f'Alumno {usuario_obj.username} inscrito en {programa_seleccionado.nombre}')
            return redirect('inscripcion') 
            
        except Exception as e:
            print(f"Error al inscribir: {e}")
            return redirect('inscripcion')

    # SI ES GET: Significa que apenas estamos entrando a la pantalla de confirmar
    else:
        # Buscamos a TODAS las personas para llenar la lista desplegable
        lista_personas = models.datos_personales.objects.filter(estatus = True)
        
        context = { 
            'programa': programa_seleccionado,
            'personas': lista_personas
        }
        # Renderizamos la plantilla que te pasé en el mensaje anterior
        return render(request, 'confirmar_inscripcion.html', context)
    
def persona(request):
    personas = models.datos_personales.objects.all()
    for i in personas:
        print (f'{i.id_user.username} {i.id_user.id}')
    return render(request, 'modulo_persona.html', {'personas':personas})

def crear_persona(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        cedula = request.POST.get('cedula')

        print(f'{cedula} {nombre}')
        correo = f'{nombre}@gmail.com'
        usuario = User.objects.create(
            password = 1234,
            email = correo
        )

    # se crea la relacion con el usuario 

        print('se creo el usuario')
        datos = models.datos_personales(
            id_user = usuario,
            cedula = cedula,
            nombre = nombre,
        )
        datos.save()
        print('se creo los datos ')

        return redirect('persona')
    else:
        return render(request, 'crear_persona.html')
    

def editar_persona(request, id):

    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            cedula = request.POST.get('cedula')
            estatus_post = request.POST.get('estatus') 
            print(f'{nombre} {cedula} {estatus_post} {type(id)} : {id}')
            
            print('Nombre de usuario actualizado.')
            
            models.datos_personales.objects.filter(id_user_id=id).update(
                cedula=cedula,
                nombre = nombre,
                estatus=int(estatus_post) 
            )
            
            print('Datos personales actualizados.')
            return redirect('persona')
            
        except Exception as e:
            print(f'ERROR DE ACTUALIZACIÓN: {e}')
            return redirect('persona')

    else:
        user = User.objects.get(id = id)
        usuario = models.datos_personales.objects.filter(id_user = user)
        if usuario.exists:
            user = models.datos_personales.objects.get(id_user = user)
            print (f'el usuario existe continue {type(user)}')
            
        else:
            print('no hay usuario ')
            return redirect('modulo_persona')
        return render(request, 'editar_persona.html', {'usuario':user})

from .utils import render_to_pdf 

# --- Al final del archivo agrega la nueva vista ---

def reporte_asistencia_pdf(request, programa_id):
    # 1. Buscamos el programa
    programa = get_object_or_404(models.Programa, id=programa_id)
    
    # 2. Buscamos los módulos de ese programa (ordenados por fecha)
    modulos = programa.modulos.all().order_by('fecha')
    
    # 3. Buscamos a los estudiantes inscritos
    inscripciones = models.Inscripcion.objects.filter(programa=programa)
    
    # 4. ARMAMOS LA MATRIZ DE DATOS
    # Queremos una estructura así: 
    # [ {alumno: "Juan", asistencias: [True, False, None]}, ... ]
    
    datos_reporte = []
    
    for inscripcion in inscripciones:
        fila_alumno = {
            'nombre': inscripcion.usuario.datos_personales.nombre,
            'cedula': inscripcion.usuario.datos_personales.cedula,
            'estados_asistencia': [] # Aquí guardaremos Si/No para cada módulo
        }
        
        # Para este alumno, revisamos módulo por módulo
        for mod in modulos:
            # Buscamos si existe registro
            try:
                asistencia = models.Asistencia.objects.get(inscripcion=inscripcion, modulo=mod)
                if asistencia.asistio:
                    estado = "ASISTIÓ"
                else:
                    estado = "FALTÓ"
            except models.Asistencia.DoesNotExist:
                estado = "-" # No se ha tomado lista aún
            
            fila_alumno['estados_asistencia'].append(estado)
            
        datos_reporte.append(fila_alumno)

    # 5. Preparamos el contexto para el HTML
    context = {
        'programa': programa,
        'modulos': modulos,
        'datos': datos_reporte,
    }
    
    # 6. Generamos el PDF usando nuestra utilidad
    return render_to_pdf('reporte_pdf.html', context)