from rest_framework import serializers
from .models import Cliente, Consulta, Tema, HistorialInteraccion, Usuario, Rol



class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['tel', 'nombre_completo', 'correo']

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id_rol', 'nombre_rol', 'descripcion']

class UsuarioSerializer(serializers.ModelSerializer):
    id_rol = RolSerializer(read_only=True)

    class Meta:
        model = Usuario
        fields = ['id_usuario', 'nombre_completo', 'correo', 'contraseña', 'id_rol', 'activo_usuario', 'fecha_creacion', 'fecha_baja']

class TemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tema
        fields = ['id_tema', 'nombre_tema', 'detalle_respuesta', 'tema_padre_id', 'orden', 'activo_tema', 'requiere_referencia']

class ConsultaSerializer(serializers.ModelSerializer):
    tema = serializers.PrimaryKeyRelatedField(queryset=Tema.objects.all())
    tema_nombre = serializers.SerializerMethodField()
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())

    class Meta:
        model = Consulta
        fields = [
            'id_consulta', 'agente', 'tema', 'tema_nombre', 'tipo', 'estado',
            'referencia_tramite', 'referencia_informada', 'fecha_creacion',
            'fecha_cierre', 'observaciones_usuario'
        ]

    def get_tema_nombre(self, obj):
        return obj.tema.nombre_tema if obj.tema else None


class HistorialInteraccionSerializer(serializers.ModelSerializer):
    consulta = ConsultaSerializer(read_only=True)

    class Meta:
        model = HistorialInteraccion
        fields = ['id_historial', 'consulta', 'mensaje_agente', 'respuesta_sistema', 'timestamp']