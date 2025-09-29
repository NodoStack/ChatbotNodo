console.log("👋 temas_arbol.js cargado correctamente");

function crearElementoTema(tema, nivel = 0) {
  const contenedor = document.createElement("div");
  contenedor.classList.add("tema-bloque");
  contenedor.style.paddingLeft = `${nivel * 20}px`;

  const enlace = document.createElement("a");
  enlace.href = "#";
  enlace.textContent = tema.nombre;
  enlace.classList.add("tema-link");
  enlace.dataset.id = tema.id;

  contenedor.appendChild(enlace);

  // Renderiza los subtemas si hay
  if (tema.subtemas && tema.subtemas.length > 0) {
    tema.subtemas.forEach(sub => {
      const hijo = crearElementoTema(sub, nivel + 1);
      contenedor.appendChild(hijo);
    });
  }

  return contenedor;
}

// 🧠 Todo lo que depende del DOM y del JSON se carga acá
document.addEventListener("DOMContentLoaded", () => {
  console.log("📦 Iniciando árbol de temas");

  const scriptDatos = document.getElementById("datos-temas");
  if (!scriptDatos) {
    console.error("❌ No se encontró el script con ID 'datos-temas'");
    return;
  }

  let datosTemas;
  try {
    datosTemas = JSON.parse(scriptDatos.textContent);
  } catch (e) {
    console.error("❌ Error al parsear datosTemas:", e);
    return;
  }

  console.log("✅ datosTemas recibido:", datosTemas);
  console.log("🧠 Cantidad de temas:", datosTemas.length);

  const contenedorArbol = document.getElementById("arbol-temas");
  if (!contenedorArbol) {
    console.error("❌ contenedorArbol no encontrado");
    return;
  }

  datosTemas.forEach(tema => {
    const bloque = crearElementoTema(tema);
    contenedorArbol.appendChild(bloque);
  });

  // ✅ Delegación de eventos para detectar clics en temas
  contenedorArbol.addEventListener("click", function (e) {
    const link = e.target.closest(".tema-link");
    if (!link) return;

    e.preventDefault();
    const temaId = link.dataset.id;
    console.log("🖱️ Click detectado en tema:", temaId);

    fetch(`/panel/temas/obtener/${temaId}/`)
      .then(res => res.json())
      .then(data => {
        
        console.log("📦 Datos recibidos del backend:", data);
        console.log("🔍 requiere_referencia:", data.requiere_referencia);
        console.log("🧪 Tipo de requiere_referencia:", typeof data.requiere_referencia);


        document.getElementById("tema-id").value = data.id_tema;
        document.getElementById("id_nombre_tema").value = data.nombre_tema;
        document.getElementById("id_orden").value = data.orden ?? '';
        document.getElementById("id_tema_padre").value = data.padre ?? '';
        document.getElementById("id_detalle_respuesta").value = data.detalle_respuesta ?? '';
        document.getElementById("form-title").textContent = "Editar Tema";
        document.getElementById("tema-form").removeAttribute("action");
        
        const checkbox = document.getElementById("id_requiere_referencia");
        checkbox.checked = (
          data.requiere_referencia === true ||
          data.requiere_referencia === "True" ||
          data.requiere_referencia === "true" ||
          data.requiere_referencia === 1 ||
          data.requiere_referencia === "1"
          );

        
        if (typeof modoVerTema === "function") {
          console.log("✅ Ejecutando modoVerTema desde delegación");

          setTimeout(() => {
             try {
                modoVerTema();
             } catch (err) {
               console.error("❌ Error al ejecutar modoVerTema:", err);
             }
          }, 200);
       } else {
         console.warn("⚠️ modoVerTema no está disponible");
       }
      });
  });
});