from django.urls import path
from asistencia import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logueado/', views.logueado, name='logueado'),
    path('logout_views/', views.logout_views, name="logout_views"),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('persona/', views.persona, name='persona'),
    path('crear_persona/', views.crear_persona, name='crear_persona'),
    path('editar_persona/<int:id>', views.editar_persona, name='editar_persona'),
    path('eliminar_persona/<int:id>', views.eliminar_persona, name='eliminar_persona'),

    path('programa/', views.programa, name='programa'),
    path('crear_programa/', views.crear_programa, name="crear_programa"), 
    path('detalle_programas/<int:id>', views.detalle_programas, name="detalle_programas"),
    path('editar_programa/<int:id>', views.editar_programa, name="editar_programa"),
    path('eliminar_programa/<int:id>', views.eliminar_programa, name="eliminar_programa"),
    path('crear_modulo/<int:id>', views.crear_modulo, name="crear_modulo"),
    path('editar_modulo/<int:id>', views.editar_modulo, name="editar_modulo"),
    path('eliminar_modulo/<int:id>', views.eliminar_modulo, name="eliminar_modulo"),
    path('reporte_pdf/<int:programa_id>/', views.reporte_asistencia_pdf, name='reporte_asistencia_pdf'),
    path('inscripcion/', views.inscripcion, name='inscripcion'),
    
    path('inscripcion/seleccionar/', views.vista_seleccionar_programa, name='vista_seleccionar_programa'),
    path('inscripcion/guardar/<int:id>/', views.inscribir_programa, name='inscribir_programa'),

    path('asistencia/', views.asistencia, name='asistencia'),
    
    path('asistencia/registrar/<int:id>/', views.registrar_asistencia, name='registrar_asistencia'),
    path('asistencia/guardar/<int:id>/', views.guardar_asistencia, name='guardar_asistencia'),
]