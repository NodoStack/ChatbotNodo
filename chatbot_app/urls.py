from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClienteViewSet, ConsultaViewSet, TemaViewSet, HistorialInteraccionViewSet,
    UsuarioViewSet, RolViewSet,
    webhook_chatbot, panel_admin, vista_inicio, vista_consultas, vista_temas, editar_tema, eliminar_tema, obtener_tema
)

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'consultas', ConsultaViewSet)
router.register(r'temas', TemaViewSet)
router.register(r'historiales', HistorialInteraccionViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'roles', RolViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('webhook_chatbot/', webhook_chatbot, name='webhook_chatbot'),
    
    # Panel
    path('panel/', panel_admin, name='panel_admin'),
    path('panel/inicio/', vista_inicio, name='vista_inicio'),
    path('panel/consultas/', vista_consultas, name='vista_consultas'),
    path('panel/temas/', vista_temas, name='vista_temas'),
    path('panel/temas/editar/<int:tema_id>/', editar_tema, name='editar_tema'),
    path('panel/temas/eliminar/<int:tema_id>/', eliminar_tema, name='eliminar_tema'),
    path('panel/temas/obtener/<int:id_tema>/', obtener_tema, name='obtener_tema'),

]
