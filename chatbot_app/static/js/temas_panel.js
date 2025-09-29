/**
 * 📂 temas_panel.js
 * Lógica específica de la vista de administración de temas.
 * - Maneja el clic en temas y subtemas del árbol.
 * - Carga los datos del tema en el formulario.
 * - Ejecuta el modo visual correspondiente (modoVerTema).
 * - Controla la acción de eliminar un tema.
 * Este archivo depende de funciones globales definidas en formulario.js.
 */

document.addEventListener("DOMContentLoaded", function () {
  // 📋 CLICK EN TEMA O SUBTEMA
  document.querySelectorAll(".tema-link").forEach(link => {
    link.addEventListener("click", e => {
      e.preventDefault();
      const temaId = link.dataset.id;

      fetch(`/panel/temas/obtener/${temaId}/`)
        .then(res => res.json())
        .then(data => {
          document.getElementById("tema-id").value = data.id_tema;
          document.getElementById("id_nombre_tema").value = data.nombre_tema;
          document.getElementById("id_orden").value = data.orden ?? '';
          document.getElementById("id_tema_padre").value = data.padre ?? '';
          document.getElementById("id_detalle_respuesta").value = data.detalle_respuesta ?? '';
          
          const checkbox = document.getElementById("id_requiere_referencia");
          checkbox.checked = (
             data.requiere_referencia === true ||
             data.requiere_referencia === "True" ||
             data.requiere_referencia === "true" ||
             data.requiere_referencia === 1 ||
             data.requiere_referencia === "1"
          );
          document.getElementById("form-title").textContent = "Editar Tema";
          document.getElementById("tema-form").setAttribute("action", `/panel/temas/editar/${data.id_tema}/`);

          setTimeout(() => {
            console.log("Cargando tema:", data);
            modoVerTema(); // función definida en formulario.js
          }, 50);
        });
    });
  });

  // 🗑️ ELIMINAR
  document.getElementById("btn-eliminar").addEventListener("click", () => {
    const temaId = document.getElementById("tema-id").value;

    if (!temaId) return;

    if (confirm("¿Estás seguro que querés eliminar este tema?")) {
      fetch(`/panel/temas/eliminar/${temaId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
        }
      })
      .then(res => {
        if (res.redirected) {
          window.location.href = res.url;
        }
      });
    }
  });
});