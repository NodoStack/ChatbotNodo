from django.db import models

   
    
class Cliente(models.Model):
    id_cliente= models.AutoField(primary_key=True)
    nombre= models.CharField(max_length=100)
    apellido= models.CharField(max_length=100)
    correo = models.EmailField()
    tel=  models.CharField(max_length=30)
    activo = models.BooleanField(default=True) 


    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre_rol

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre_completo = models.CharField(max_length=150)
    correo = models.EmailField()
    contraseña = models.CharField(max_length=128)  
    id_rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    activo_usuario = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_baja = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.nombre_completo
    
class Tema(models.Model):
    id_tema = models.AutoField(primary_key=True)
    nombre_tema = models.CharField(max_length=150)
    detalle_respuesta = models.TextField(blank=True, null=True)
    # Si tema_padre es NULL, significa que este tema es un tema padre (nivel superior)
    tema_padre = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subtemas'
    )
    orden = models.IntegerField(default=0)
    activo_tema = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre_tema
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nombre_tema', 'tema_padre'],
                name='unique_nombre_por_padre'
            )
        ]
    """
    🔹 Representación textual del tema.
    🔹 Construye la jerarquía completa del tema desde el raíz hasta el actual.
    🔹 Ejemplo: 'Ausentismo / Edificio Alvear / Secretaría de Niñez'
    🔹 Útil para mostrar la estructura completa en el panel de administración o en logs.
    """



class Consulta(models.Model):
    TIPO_CONSULTA_CHOICES = [
        ('consulta', 'Consulta'),
        ('tramite', 'Trámite iniciado'),
    ]

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('resuelto', 'Resuelto'),
        ('redireccionado', 'Redireccionado'),
    ]

    id_consulta = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tema = models.ForeignKey(Tema, on_delete=models.SET_NULL, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(blank=True, null=True)
    observaciones_usuario = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Consulta {self.id_consulta} - {self.cliente.apellido} {self.cliente.nombre}"


class HistorialInteraccion(models.Model):
    id_historial = models.AutoField(primary_key=True)
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='interacciones')
    mensaje_cliente = models.TextField(blank=True, null=True)
    respuesta_sistema = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interacción {self.id_historial} Consulta {self.consulta.id_consulta}"