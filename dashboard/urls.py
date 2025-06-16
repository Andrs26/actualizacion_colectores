from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('clientes/', views.clientes, name='clientes_admin'),
    path('cliente/<int:cliente_id>/', views.detalle_cliente_admin, name='detalle_cliente_admin'),
    path('cliente/<int:cliente_id>/ver', views.ver_detalle_cliente_admin, name='ver_detalle_cliente_admin'),
    path('exportar/', views.exportar_home, name='exportar_home'),
    path('exportar_clientes_excel/', views.exportar_clientes_excel, name='exportar_excel'),
    path('exportar_clientes_datos_excel/', views.exportar_clientes_datos_excel, name='exportar_clientes_datos'),
    path('exportar_clientes_contactos_excel/', views.exportar_clientes_contactos_excel, name='exportar_clientes_contactos'),
    path('importar/', views.importar_home, name='importar_home'),
    path('importar_clientes_excel/', views.importar_clientes_excel, name='importar_clientes_excel'),
    path('importar_clientes_datos_excel/', views.importar_clientes_datos_excel, name='importar_clientes_datos_excel'),
    path('importar_clientes_contactos_excel/', views.importar_clientes_contactos_excel, name='importar_clientes_contactos_excel'),
    path('asignar/', views.asignar_usuarios_pendientes, name='asignar_usuarios_pendientes'),
    path('resumen-asignacion/', views.resumen_asignacion_json, name='resumen_asignacion_json'),
    path('importar-clientes/', views.carga_inicial_clientes, name='carga_inicial_clientes'),
    path('clientes/asignar/', views.asignar_clientes_masivo, name='asignar_clientes_masivo'),
    path('clientes/reasignar/', views.reasignar_cliente, name='reasignar_cliente'),
]
