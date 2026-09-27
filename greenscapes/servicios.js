const API = "http://127.0.0.1:8000";

// Pido los servicios a la API y pongo cada uno en la sección de su categoría
fetch(API + "/ver_servicios")
    .then(res => res.json())
    .then(servicios => {
        servicios.forEach(s => {
            const lista = document.getElementById("lista_" + s.categoria.toLowerCase());
            if (!lista) return;

            lista.innerHTML += `
                <div class="card">
                    <h3>${s.servicio}</h3>
                    <p>${s.descripcion}</p>
                    <span class="precio">$ ${s.precio.toLocaleString("es-AR")}</span>
                </div>
            `;
        });
    })
    .catch(() => alert("No se pudo conectar con la API. ¿Está corriendo uvicorn?"));
