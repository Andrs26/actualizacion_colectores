

from django.urls import path
from . import views

urlpatterns = [
    path('asignados/', views.asignacion_usuario, name='asignacion_usuario'),
    path('cliente/<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente'),
    path('cliente/<int:cliente_id>/ver', views.ver_detalle_cliente, name='ver_detalle_cliente'),
    path('cliente/<int:cliente_id>/editar/', views.editar_cliente, name='editar_cliente'),
    path('cliente/<int:cliente_id>/actualizar/', views.actualizar_cliente, name='actualizar_cliente'),
    path('cliente/<int:cliente_id>/no-ubicado/', views.marcar_no_ubicado, name='marcar_no_ubicado'),
]