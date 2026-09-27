const API = "http://127.0.0.1:8000";
let servicios = [];

// Trae los servicios y arma la tabla
function cargar() {
    fetch(API + "/ver_servicios")
        .then(res => res.json())
        .then(datos => {
            servicios = datos;
            let filas = "";
            servicios.forEach(s => {
                filas += `
                    <tr>
                        <td>${s.servicio}</td>
                        <td>${s.categoria}</td>
                        <td>$ ${s.precio.toLocaleString("es-AR")}</td>
                        <td>
                            <button class="btn chico" onclick="editar(${s.id})">Editar</button>
                            <button class="btn chico rojo" onclick="borrar(${s.id})">Borrar</button>
                        </td>
                    </tr>
                `;
            });
            document.getElementById("tabla").innerHTML = filas;
        })
        .catch(() => mostrar("No se pudo conectar con la API. ¿Está corriendo uvicorn?"));
}

// Agrega o edita, según si hay un id cargado
function guardar(event) {
    event.preventDefault();

    const id = document.getElementById("id").value;
    const datos = {
        servicio: document.getElementById("servicio").value,
        descripcion: document.getElementById("descripcion").value,
        precio: Number(document.getElementById("precio").value),
        categoria: document.getElementById("categoria").value
    };

    let url = API + "/agregar_servicios";
    let metodo = "POST";
    if (id) {
        url = API + "/editar_servicio/" + id;
        metodo = "PUT";
    }

    fetch(url, {
        method: metodo,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos)
    })
        .then(res => res.json())
        .then(respuesta => {
            mostrar(respuesta.mensaje || respuesta.detail);
            limpiar();
            cargar();
        });
}

// Pasa los datos del servicio al formulario
function editar(id) {
    const s = servicios.find(s => s.id === id);
    document.getElementById("id").value = s.id;
    document.getElementById("servicio").value = s.servicio;
    document.getElementById("descripcion").value = s.descripcion;
    document.getElementById("precio").value = s.precio;
    document.getElementById("categoria").value = s.categoria;
    document.getElementById("titulo_form").textContent = "Editar servicio";
    window.scrollTo({ top: 0, behavior: "smooth" });
}

function borrar(id) {
    if (!confirm("¿Seguro que querés borrar este servicio?")) return;

    fetch(API + "/borrar_servicio/" + id, { method: "DELETE" })
        .then(res => res.json())
        .then(respuesta => {
            mostrar(respuesta.mensaje || respuesta.detail);
            cargar();
        });
}

function limpiar() {
    document.getElementById("formulario").reset();
    document.getElementById("id").value = "";
    document.getElementById("titulo_form").textContent = "Agregar servicio";
}

function mostrar(texto) {
    document.getElementById("mensaje").textContent = texto;
}

cargar();
