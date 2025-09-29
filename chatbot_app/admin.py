from django.contrib import admin
from .models import Cliente, Consulta, Tema, HistorialInteraccion, Usuario, Rol


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id_cliente', 'nombre', 'apellido', 'correo', 'tel', 'activo')
    search_fields = ('nombre', 'apellido', 'tel', 'correo')
    list_filter = ('activo',)


class TemaAdmin(admin.ModelAdmin):
    list_display = ('id_tema', 'nombre_tema', 'activo_tema', 'orden', 'tema_padre')
    search_fields = ('nombre_tema',)
    list_filter = ('activo_tema', )


class ConsultaAdmin(admin.ModelAdmin):

    def mostrar_tema(self, obj):
        return obj.tema.nombre_tema if obj.tema else "-"
    mostrar_tema.short_description = "Tema"

    readonly_fields = ('fecha_creacion',)
    list_display = ('id_consulta', 'cliente', 'tema', 'fecha_creacion', 'estado')
    search_fields = ('cliente__nombre', 'cliente__apellido', 'tema__nombre_tema')
    list_filter = ('estado', 'fecha_creacion')

    fields = (
        'cliente', 'tema', 'estado',
        'fecha_creacion', 'fecha_cierre', 'observaciones_usuario'
    )
admin.site.register(Cliente)
admin.site.register(Consulta, ConsultaAdmin)
admin.site.register(Tema, TemaAdmin)
admin.site.register(HistorialInteraccion)
admin.site.register(Usuario)
admin.site.register(Rol)