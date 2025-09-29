from django import forms
from .models import Tema

class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = [
            'nombre_tema',
            'detalle_respuesta',
            'tema_padre',
            'orden',
            'activo_tema',
                    ]
        widgets = {
            'nombre_tema': forms.TextInput(attrs={'class': 'form-control'}),
            'detalle_respuesta': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tema_padre': forms.Select(attrs={'class': 'form-control'}),
            'orden': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    # 🧪 Validación de duplicado y ciclo
    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get("nombre_tema")
        padre = cleaned_data.get("tema_padre")

        print("🧪 Ejecutando clean()")

        if nombre:
            nombre_normalizado = nombre.strip().lower()

            print("🔍 Nombre normalizado para validar:", nombre_normalizado)
            print("🔍 Padre recibido:", padre)

            # 🔍 Validación manual de duplicado
            for t in Tema.objects.exclude(id_tema=self.instance.id_tema):
                nombre_existente = t.nombre_tema.strip().lower()
                padre_existente = t.tema_padre

                print("🔍 Comparando con:", nombre_existente, "padre:", padre_existente)

                if nombre_existente == nombre_normalizado and padre_existente == padre:
                    self.add_error("nombre_tema", "❌ Ya existe un tema con ese nombre en este nivel.")
                    break

        # 🔁 Validación de ciclo
        tema = self.instance
        actual = padre
        while actual:
            if actual == tema:
                self.add_error("tema_padre", "❌ Este tema no puede ser su propio padre.")
                break
            actual = actual.tema_padre

        return cleaned_data