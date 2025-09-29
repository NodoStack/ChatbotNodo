/**
 * 📝 formulario.js
 * Lógica del formulario de administración de temas en el panel del chatbot.
 * Controla los modos de visualización (ver, nuevo, editar), el estado de los campos,
 * y la visibilidad de los botones según la acción del usuario.
 * Este archivo debe cargarse junto con temas_arbol.js en la vista temas.html.
 */

// 🔗 Referencias globales
const formFields = document.querySelectorAll("#tema-form input, #tema-form select, #tema-form textarea");


const btnNuevo = document.getElementById("btn-nuevo");
const btnEditar = document.getElementById("btn-editar");
const btnGuardar = document.getElementById("btn-guardar");
const btnEliminar = document.getElementById("btn-eliminar");
const btnCancelar = document.getElementById("btn-cancelar");

// 🔒 Deshabilita todos los campos del form
function deshabilitarCampos() {
  formFields.forEach(field => field.setAttribute("disabled", true));
}

// 🔓 Habilita todos los campos del form
function habilitarCampos() {
  formFields.forEach(field => field.removeAttribute("disabled"));
}

// ✏️ Modo Ver Tema
function modoVerTema() {
  deshabilitarCampos();
  btnNuevo.classList.add("d-none");
  btnEditar.classList.remove("d-none");
  btnGuardar.classList.add("d-none");
  btnEliminar.classList.remove("d-none");
  btnCancelar.classList.remove("d-none");
  console.log("Modo actual: Ver Tema");
}

// 🔄 Resetea el formulario
function resetForm() {
  document.getElementById("tema-form").reset();
  document.getElementById("tema-id").value = "";
  document.getElementById("form-title").textContent = "Agregar / Editar Tema";
}

// 🎯 Modo inicial (solo botón nuevo)
function modoInicio() {
  deshabilitarCampos();
  resetForm();
  btnNuevo.classList.remove("d-none");
  btnEditar.classList.add("d-none");
  btnGuardar.classList.add("d-none");
  btnEliminar.classList.add("d-none");
  btnCancelar.classList.add("d-none");
  console.log("Modo actual: Ver Tema");
  document.getElementById("form-title").textContent = "Ver Tema";

  // 🧼 Elimina errores visuales del formulario:
  document.querySelectorAll('.errorlist, .error-validacion').forEach(el => el.remove());

}

// 🟢 Modo Nuevo Tema
function modoNuevo() {
  habilitarCampos();
  resetForm();
  document.getElementById("form-title").textContent = "Agregar Tema";
  btnNuevo.classList.add("d-none");
  btnEditar.classList.add("d-none");
  btnGuardar.classList.remove("d-none");
  btnEliminar.classList.add("d-none");
  btnCancelar.classList.remove("d-none");
  document.getElementById("tema-form").removeAttribute("action");
  console.log("Modo actual: Ver Tema");
}

// 🛠️ Modo Editar Tema
function modoEditar() {
  habilitarCampos();
  btnEditar.classList.add("d-none");
  btnGuardar.classList.remove("d-none");
  btnCancelar.classList.remove("d-none");
  console.log("Modo actual: Ver Tema");
  
}

// ✅ Exponer funciones globalmente
window.modoVerTema = modoVerTema;
window.modoInicio = modoInicio;
window.modoNuevo = modoNuevo;
window.modoEditar = modoEditar;

// 🧩 Asignar eventos a botones
document.addEventListener("DOMContentLoaded", function () {
  btnNuevo.addEventListener("click", modoNuevo);
  btnEditar.addEventListener("click", modoEditar);
  btnCancelar.addEventListener("click", modoInicio);
});

// ESPERA QUE EL DOM ESTE LISTO, BUSCA SI HAY ERRORES EN EL FORMULARIO..
//SI LOS HAY MUESTRA EL BOTON CANCELAR
document.addEventListener('DOMContentLoaded', function () {
  const hayErrores = document.querySelector('.error-validacion');
if (hayErrores) {
  modoErrorValidacion();
}
});

function modoErrorValidacion() {
  habilitarCampos();
  btnNuevo.classList.add("d-none");
  btnEditar.classList.add("d-none");
  btnGuardar.classList.remove("d-none");
  btnEliminar.classList.add("d-none");
  btnCancelar.classList.remove("d-none");
  document.getElementById("form-title").textContent = "Agregar Tema";
  console.log("⚠️ Modo actual: Error de validación");
}

function limpiarErroresValidacion() {
  document.querySelectorAll(".error-validacion").forEach(e => e.remove());
}
document.querySelectorAll("#tema-form input, #tema-form select, #tema-form textarea").forEach((campo) => {
  campo.addEventListener("input", limpiarErroresValidacion);
});

// ✅ Inicializa y muestra los mensajes tipo toast del backend (éxito, error, etc.)
document.addEventListener('DOMContentLoaded', function () {
  const toastElList = [].slice.call(document.querySelectorAll('.toast'));
  toastElList.forEach(function (toastEl) {
    const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
    toast.show();
  });
});