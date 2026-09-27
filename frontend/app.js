// Dirección donde corre el backend de FastAPI
const API = "http://127.0.0.1:8000";

// Acá guardamos todos los servicios que trae la API
let servicios = [];
// Categoría elegida en los filtros ("" = todas)
let categoriaActual = "";
// Para poder cancelar el temporizador del aviso anterior
let timerToast = null;

// Elementos de la página que vamos a usar
const lista = document.getElementById("lista-servicios");
const estado = document.getElementById("estado");
const filtros = document.getElementById("filtros");
const form = document.getElementById("form-servicio");
const formTitulo = document.getElementById("form-titulo");
const inputId = document.getElementById("servicio-id");
const inputServicio = document.getElementById("servicio");
const inputDescripcion = document.getElementById("descripcion");
const inputPrecio = document.getElementById("precio");
const inputCategoria = document.getElementById("categoria");
const btnCancelar = document.getElementById("btn-cancelar");
const toast = document.getElementById("toast");

// Muestra un mensaje flotante por 3 segundos
function mostrarToast(texto, esError) {
  clearTimeout(timerToast);
  toast.textContent = texto;
  toast.classList.add("visible");
  toast.classList.toggle("toast--error", Boolean(esError));
  timerToast = setTimeout(() => {
    toast.classList.remove("visible", "toast--error");
  }, 3000);
}

// Cambia el texto de estado (y lo pone en rojo si es un error)
function mostrarEstado(texto, esError) {
  estado.textContent = texto;
  estado.classList.toggle("estado--error", Boolean(esError));
}

// Pasa un número a formato de pesos argentinos: 60000 -> "$ 60.000"
function formatearPrecio(precio) {
  return "$ " + Number(precio).toLocaleString("es-AR", { maximumFractionDigits: 0 });
}

// Crea un elemento con una clase y un texto (textContent evita inyectar HTML)
function crear(etiqueta, clase, texto) {
  const el = document.createElement(etiqueta);
  el.className = clase;
  if (texto !== undefined) el.textContent = texto;
  return el;
}

// Arma la tarjeta de un servicio
function crearCard(s) {
  const card = crear("article", "card");
  card.dataset.categoria = s.categoria;

  const btnEditar = crear("button", "btn-editar", "Editar");
  btnEditar.dataset.id = s.id;
  const btnBorrar = crear("button", "btn-borrar", "Borrar");
  btnBorrar.dataset.id = s.id;

  const acciones = crear("div", "card-acciones");
  acciones.append(btnEditar, btnBorrar);

  const pie = crear("div", "card-pie");
  pie.append(crear("span", "card-precio", formatearPrecio(s.precio)), acciones);

  card.append(
    crear("span", "card-categoria", s.categoria),
    crear("h3", "card-titulo", s.servicio),
    crear("p", "card-descripcion", s.descripcion),
    pie
  );
  return card;
}

// Dibuja la lista según la categoría elegida (sin volver a pedir a la API)
function mostrarServicios() {
  const filtrados = servicios.filter(
    (s) => categoriaActual === "" || s.categoria === categoriaActual
  );
  lista.innerHTML = "";
  if (filtrados.length === 0) {
    mostrarEstado("No hay servicios en esta categoría.");
    return;
  }
  mostrarEstado("");
  filtrados.forEach((s) => lista.appendChild(crearCard(s)));
}

// Pide los servicios a la API
async function cargarServicios() {
  mostrarEstado("Cargando servicios...");
  try {
    const respuesta = await fetch(API + "/ver_servicios");
    if (!respuesta.ok) throw new Error("Error " + respuesta.status);
    servicios = await respuesta.json();
    mostrarServicios();
  } catch (error) {
    lista.innerHTML = "";
    mostrarEstado("No se pudo conectar con la API. ¿Está corriendo uvicorn?", true);
  }
}

// Hace un pedido a la API y devuelve el JSON; si falla, lanza un error con el detalle
async function pedir(url, metodo, datos) {
  const opciones = { method: metodo, headers: { "Content-Type": "application/json" } };
  if (datos) opciones.body = JSON.stringify(datos);
  const respuesta = await fetch(API + url, opciones);
  const json = await respuesta.json().catch(() => ({}));
  if (!respuesta.ok) {
    const detalle = typeof json.detail === "string" ? json.detail : "Revisá los datos ingresados.";
    throw new Error(detalle);
  }
  return json;
}

// Deja el formulario listo para agregar un servicio nuevo
function resetearFormulario() {
  form.reset();
  inputId.value = "";
  formTitulo.textContent = "Agregar servicio";
  btnCancelar.hidden = true;
}

// Carga los datos de un servicio en el formulario para editarlo
function editarServicio(id) {
  const s = servicios.find((x) => x.id === id);
  if (!s) return;
  inputId.value = s.id;
  inputServicio.value = s.servicio;
  inputDescripcion.value = s.descripcion;
  inputPrecio.value = s.precio;
  inputCategoria.value = s.categoria;
  formTitulo.textContent = "Editar servicio";
  btnCancelar.hidden = false;
  form.scrollIntoView({ behavior: "smooth" });
}

// Pregunta y borra un servicio
async function borrarServicio(id) {
  const s = servicios.find((x) => x.id === id);
  const nombre = s ? s.servicio : "este servicio";
  if (!confirm('¿Borrar "' + nombre + '"?')) return;
  try {
    const json = await pedir("/borrar_servicio/" + id, "DELETE");
    mostrarToast(json.mensaje);
    if (inputId.value === String(id)) resetearFormulario();
    cargarServicios();
  } catch (error) {
    mostrarToast(error.message || "No se pudo borrar el servicio.", true);
  }
}

// Guardar: si no hay id se agrega (POST), si hay id se edita (PUT)
form.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const datos = {
    servicio: inputServicio.value.trim(),
    descripcion: inputDescripcion.value.trim(),
    precio: Number(inputPrecio.value),
    categoria: inputCategoria.value,
  };
  const id = inputId.value;
  try {
    const json = id
      ? await pedir("/editar_servicio/" + id, "PUT", datos)
      : await pedir("/agregar_servicios", "POST", datos);
    mostrarToast(json.mensaje);
    resetearFormulario();
    cargarServicios();
  } catch (error) {
    mostrarToast(error.message || "No se pudo guardar el servicio.", true);
  }
});

btnCancelar.addEventListener("click", resetearFormulario);

// Un solo "escuchador" para todos los botones de las tarjetas
lista.addEventListener("click", (evento) => {
  const boton = evento.target.closest("button");
  if (!boton) return;
  const id = Number(boton.dataset.id);
  if (boton.classList.contains("btn-editar")) editarServicio(id);
  if (boton.classList.contains("btn-borrar")) borrarServicio(id);
});

// Filtros por categoría
filtros.addEventListener("click", (evento) => {
  const boton = evento.target.closest("button.filtro");
  if (!boton) return;
  filtros.querySelectorAll(".filtro").forEach((b) => b.classList.remove("activo"));
  boton.classList.add("activo");
  categoriaActual = boton.dataset.categoria;
  mostrarServicios();
});

// Al abrir la página, traemos los servicios
cargarServicios();
