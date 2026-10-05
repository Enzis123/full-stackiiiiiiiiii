# GreenScapes TP FULL-STACK

### Alumno: Enzo Benjamin Romero
### Curso: 6to 5ta

**Página online:** https://greenscapesproyect.netlify.app
**API online:** https://full-stackiiiiiiiiii.onrender.com/docs

---

## ¿Qué es `GreenScapes`?

* **GreenScapes** es una empresa de mi familia. Se dedica a ofrecer servicios de mantenimiento y cuidado de `Parques`, `Piletas` y los distintos tipos de `espacios` que se encuentran en los lotes particulares o de barrios abiertos o cerrados.

* Tomé la decisión de utilizar esta empresa para desarrollar mi proyecto porque necesita una página web sobre la empresa, y otro tipo de aplicaciones para dispositivos móviles. Lo vi como el mejor ejemplo a seguir para aprender a desarrollar una app Full Stack.

* La app tiene dos partes:
  * Una **página pública** (`index.html`) donde se ven todos los servicios separados en **Parque, Pileta y Mantenimiento**, con su descripción y precio.
  * Un **panel de administración** (`admin.html`) donde se pueden **agregar, editar y borrar** servicios.

* La entidad principal es el **servicio**, que tiene 5 campos:

| Campo | Tipo | Ejemplo |
|---|---|---|
| `id` | entero (lo pone SQLite solo) | `3` |
| `servicio` | texto | `"corte de pasto"` |
| `descripcion` | texto | `"corte de 150m2"` |
| `precio` | número decimal | `120000.0` |
| `categoria` | texto (`Parque`, `Pileta` o `Mantenimiento`) | `"Parque"` |

---

## Estructura del proyecto

```
full-stackiiiiiiiiii/
├── README.md
├── backend/
│   ├── main.py                  → app FastAPI, rutas y CORS
│   ├── models/
│   │   └── modelServicios.py    → modelo Pydantic
│   ├── managers/
│   │   └── manager.py           → consultas SQL (listar, crear, buscar, editar, borrar)
│   ├── database/
│   │   ├── database_conn.py     → conexión (get_db) y creación de la tabla
│   │   └── db.db                → base de datos SQLite
│   └── requirements.txt
├── greenscapes/                 → frontend
│   ├── index.html + servicios.js
│   ├── admin.html + admin.js
│   └── style.css
└── docs/
    ├── capturas/
    └── graficos/
```

---

## Instalación y ejecución

Se necesita **Python 3.10 o más nuevo** y **Git**.

**1. Clonar el repositorio**

```bash
git clone https://github.com/Enzis123/full-stackiiiiiiiiii.git
cd full-stackiiiiiiiiii
```

**2. Crear el entorno virtual e instalar las dependencias**

```bash
python -m venv env
env\Scripts\activate          # en Linux / Mac: source env/bin/activate
pip install -r backend/requirements.txt
```

**3. Levantar la API**

```bash
cd backend
uvicorn main:app --reload
```

La API queda en `http://127.0.0.1:8000`.

**4. Abrir el frontend**

Con la API corriendo, abrir `greenscapes/index.html` con **Live Server**

y entrar a `http://127.0.0.1:5500`. También funciona abriendo `index.html` con doble clic.

### Documentación automática (`/docs`)

FastAPI genera sola una página donde se pueden ver y probar todos los endpoints:

* Local: http://127.0.0.1:8000/docs
* Online: https://full-stackiiiiiiiiii.onrender.com/docs

> La API online está en el plan gratis de Render: si nadie la usa un rato "se duerme" y la primera petición tarda unos segundos. Además, los cambios que se hagan en la base online se pierden cuando Render reinicia el servidor.

---

## Endpoints

| Método | Ruta | Qué hace |
|---|---|---|
| `GET` | `/ver_servicios` | Lista todos los servicios |
| `GET` | `/ver_servicio/{id}` | Busca un servicio por su id |
| `POST` | `/agregar_servicios` | Crea un servicio nuevo |
| `PUT` | `/editar_servicio/{id}` | Edita un servicio |
| `DELETE` | `/borrar_servicio/{id}` | Borra un servicio |

### `GET /ver_servicios`

Respuesta `200`:

```json
[
  {"id": 3, "servicio": "corte de pasto", "descripcion": "corte de 150m2", "precio": 120000.0, "categoria": "Parque"},
  ...
]
```

### `GET /ver_servicio/{id}`

`GET /ver_servicio/3` → `200`:

```json
{"id": 3, "servicio": "corte de pasto", "descripcion": "corte de 150m2", "precio": 120000.0, "categoria": "Parque"}
```

Si el id no existe → `200`:

```json
{"mensaje": "No existe un servicio con ese id"}
```

### `POST /agregar_servicios`

Body:

```json
{"servicio": "Corte de cesped", "descripcion": "Corte y bordeado", "precio": 25000, "categoria": "Parque"}
```

Respuesta `200`:

```json
{"mensaje": "Servicio agregado"}
```

### `PUT /editar_servicio/{id}`

`PUT /editar_servicio/3` con body:

```json
{"servicio": "Corte de cesped XL", "descripcion": "Lotes grandes", "precio": 40000, "categoria": "Parque"}
```

Respuesta `200`:

```json
{"mensaje": "Servicio editado"}
```

### `DELETE /borrar_servicio/{id}`

`DELETE /borrar_servicio/3` → `200`:

```json
{"mensaje": "Servicio borrado"}
```

### Si los datos están mal → `422`

Si en `POST` o `PUT` falta un campo o un campo tiene un tipo equivocado, la API responde `422` (ver el ejemplo en la Pregunta 6).

---

## Preguntas de arquitectura

### Pregunta 1 — El ciclo de vida de una petición

![Solicitud Guardar](docs/graficos/solicitud-guardar.png)

Paso a paso, cuando el usuario hace clic en **Guardar** en el panel de administración:

1. El usuario completa el formulario y hace clic en **Guardar**. El formulario llama a la función `guardar(event)` de `admin.js`, y `event.preventDefault()` evita que la página se recargue.
2. `admin.js` lee lo que se escribió en cada campo y arma un objeto con `servicio`, `descripcion`, `precio` y `categoria`.
3. Con `fetch` el navegador manda una petición **`POST /agregar_servicios`** a la API, con el objeto convertido a texto JSON (`JSON.stringify`) y el header `Content-Type: application/json`.
4. La petición llega a la API (FastAPI). Antes de entrar a la función, **Pydantic** revisa que el JSON tenga todos los campos del modelo `modelServicios` y que cada uno sea del tipo correcto. Si algo está mal, la API corta ahí y devuelve `422`.
5. Si los datos están bien, FastAPI ejecuta `get_db()` (por `Depends`), que abre la conexión a SQLite y se la pasa a la ruta.
6. La ruta llama a `manager.crear(db, datos)`. El manager hace el `INSERT INTO servicios ...` y el `commit`, y así el servicio queda guardado en `db.db`.
7. El manager devuelve `{"mensaje": "Servicio agregado"}`, la API lo manda al navegador con código `200`, y al terminar la petición `get_db()` cierra la conexión.
8. `admin.js` recibe la respuesta, muestra el mensaje, limpia el formulario y vuelve a pedir la lista con `GET /ver_servicios`.
9. La API devuelve la lista de servicios en JSON y `admin.js` vuelve a armar la tabla, así el usuario ya ve el servicio nuevo.

### Pregunta 2 — ¿Quién es el cliente y quién es el servidor?

![Arquitectura](docs/graficos/arquitectura.png)

* **Cliente:** el navegador, con las páginas de la carpeta `greenscapes/` (HTML, CSS y JS). Es el que le muestra todo al usuario y el que hace los pedidos con `fetch`. Online está en **Netlify**.
* **Servidor:** la API hecha con FastAPI (carpeta `backend/`). Recibe los pedidos, valida los datos, consulta la base SQLite y responde con JSON. Online está en **Render**.

La diferencia con una aplicación de escritorio tradicional es que en una app de escritorio todo (la pantalla, la lógica y los datos) está en la misma compu y en el mismo programa. En el modelo cliente-servidor están separados y se comunican por la red con HTTP: el cliente no toca la base de datos directamente, se la tiene que pedir al servidor. Por eso muchas personas pueden usar la página desde distintos lugares y todas ven los mismos datos, porque los datos están en un solo lugar (el servidor).

### Pregunta 3 — HTTP como lenguaje común

Los **métodos HTTP** dicen qué quiere hacer el cliente:

* `GET` → pedir datos (ver los servicios).
* `POST` → crear algo nuevo (agregar un servicio).
* `PUT` → modificar algo que ya existe (editar un servicio).
* `DELETE` → borrar algo.

Los **códigos de estado** son números que manda el servidor para decir cómo salió el pedido:

* `200` OK → salió todo bien.
* `201` Created → se creó un recurso nuevo.
* `404` Not Found → lo que se pidió no existe.
* `422` Unprocessable Entity → los datos que se mandaron no son válidos.

| Operación | Método | Ruta | Código de éxito | Código de error |
|---|---|---|---|---|
| Listar | GET | `/ver_servicios` | 200 | — |
| Ver uno | GET | `/ver_servicio/{id}` | 200 | 422 (si el id no es un número) |
| Crear | POST | `/agregar_servicios` | 200 | 422 (faltan campos o tipos incorrectos) |
| Editar | PUT | `/editar_servicio/{id}` | 200 | 422 (faltan campos o tipos incorrectos) |
| Borrar | DELETE | `/borrar_servicio/{id}` | 200 | 422 (si el id no es un número) |

¿Por qué esos códigos? Las rutas de mi API devuelven lo que devuelve el manager, y FastAPI por defecto responde `200` si la función termina bien. Por eso crear también devuelve `200` y no `201`. Cuando un id no existe tampoco devuelvo `404`: la API responde `200` con un mensaje que lo avisa (`"No existe un servicio con ese id"`). El `422` no lo programé yo: lo devuelve FastAPI solo cuando Pydantic encuentra que los datos del body (o el id de la ruta) no tienen el formato correcto.

### Pregunta 4 — CORS

![CORS](docs/graficos/cors.png)

El **SOP (Same-Origin Policy)** es una regla de seguridad del navegador: una página solo puede leer respuestas de su **mismo origen**. El origen es la combinación de protocolo + dominio + puerto. Por ejemplo `https://greenscapesproyect.netlify.app` y `https://full-stackiiiiiiiiii.onrender.com` son orígenes distintos, y en local también lo son `http://127.0.0.1:5500` (Live Server) y `http://127.0.0.1:8000` (la API), porque cambia el puerto.

El navegador bloquea esto para que una página cualquiera no pueda usar tu sesión para leer datos de otro sitio sin permiso.

Como mi frontend y mi API están en orígenes distintos, necesito **CORS**. En `main.py` agregué el `CORSMiddleware` con la lista `origenes_permitidos` (la página de Netlify, Live Server en el puerto 5500 y `"null"`, que es el origen cuando se abre el HTML con doble clic). Lo que pasa es:

1. Cuando `admin.js` manda un `POST` con JSON, el navegador primero hace una pregunta (**preflight**): un `OPTIONS` con el header `Origin`.
2. El middleware se fija si ese origen está en la lista. Si está, responde `200` con el header `Access-Control-Allow-Origin`.
3. Recién ahí el navegador manda el `POST` de verdad, y la respuesta también viene con ese header, así que deja que `admin.js` lea el JSON.
4. Si el origen **no** está en la lista, el middleware responde `400 Disallowed CORS origin` y el navegador bloquea la respuesta. El `fetch` cae en el `.catch()` y en la página aparece "No se pudo conectar con la API."

### Pregunta 5 — Separación de responsabilidades

Separé el proyecto en partes, y cada una hace una sola cosa:

* `main.py` → las rutas: recibe el pedido y devuelve la respuesta.
* `modelServicios.py` → cómo tiene que ser un servicio (Pydantic).
* `manager.py` → todo el SQL (`SELECT`, `INSERT`, `UPDATE`, `DELETE`).
* `database_conn.py` → abrir y cerrar la conexión a la base.

Separar el acceso a la base (manager) de los endpoints sirve para que las rutas queden cortas y fáciles de leer, y para que, si hay que cambiar una consulta o incluso cambiar de base de datos, solo se toque el manager y no todas las rutas.

La **inyección de dependencias** es el `db=Depends(get_db)` de cada ruta. FastAPI se encarga de ejecutar `get_db()`: abre **una** conexión por petición, se la pasa a la ruta y, gracias al `try/finally`, la cierra al final aunque haya habido un error. Así no tengo que escribir el código de conectar y cerrar en cada ruta.

Si abriera una conexión nueva por cada línea de código en vez de inyectarla, el programa sería más lento, repetiría mucho código y sería fácil olvidarse de cerrar alguna conexión. Con SQLite, además, podría quedar la base bloqueada ("database is locked") por tener varias conexiones abiertas a la vez.

### Pregunta 6 — JSON como formato de intercambio

Cliente y servidor usan **JSON** porque es texto, entonces viaja bien por HTTP, y porque lo entienden los dos lados: JavaScript lo convierte con `JSON.stringify()` / `res.json()` y Python con FastAPI. Además es fácil de leer para una persona.

Cuando llega un `POST` o `PUT`, FastAPI toma el JSON del body y se lo pasa a **Pydantic**, que lo convierte en un objeto `modelServicios`. Pydantic revisa que estén los 4 campos y que cada uno sea del tipo correcto (`precio` tiene que ser un número; si llega `"25000"` como texto lo convierte a `25000.0`). La validación garantiza que al manager solo llegan datos correctos, así nunca se guarda en la base un servicio sin nombre o con un precio que no es un número.

Ejemplo de un request inválido (falta `descripcion` y el precio es texto):

```http
POST /agregar_servicios
Content-Type: application/json

{"servicio": "Corte de cesped", "precio": "abc", "categoria": "Parque"}
```

Respuesta del servidor, `422 Unprocessable Entity`:

```json
{
  "detail": [
    {"type": "missing", "loc": ["body", "descripcion"], "msg": "Field required", "input": {"servicio": "Corte de cesped", "precio": "abc", "categoria": "Parque"}},
    {"type": "float_parsing", "loc": ["body", "precio"], "msg": "Input should be a valid number, unable to parse string as a number", "input": "abc"}
  ]
}
```

En el panel, cuando llega esta respuesta, `admin.js` muestra "Revisá los datos: hay campos vacíos o inválidos." y no borra el formulario.

### Pregunta 7 — Statelessness (sin estado)

Que HTTP sea **stateless** significa que el servidor no se acuerda de las peticiones anteriores: cada petición llega sola y tiene que traer todo lo que el servidor necesita para responderla. Por ejemplo, para editar, el `PUT` trae el id en la ruta y todos los datos en el body.

En mi proyecto el "estado" (los servicios) no queda guardado en la API ni en variables de Python: queda en la base de datos **SQLite** (`backend/database/db.db`). La API abre la conexión, consulta y la cierra en cada petición.

La ventaja es que, si mañana tuviera 3 servidores en vez de 1, cualquier servidor podría atender cualquier petición, porque ninguno guarda nada propio: todos leerían y escribirían la misma base. (Para eso habría que usar una base compartida, como PostgreSQL, porque el archivo de SQLite queda en una sola compu.)

---

## Capturas

**Inicio**

![Inicio](docs/capturas/inicio.png)

**Servicios**

![Servicios](docs/capturas/servicios.png)

**Panel de administración**

![Administrar](docs/capturas/admin.png)

**Celular**

![Celular](docs/capturas/celular.png)

---

## Criterios de Diseño

### ``Frontend``
* **Estructura**: utilicé una estructura básica, la que nos enseñaron en la clase de diseño web estático. La estructura se basa en:

  ```
  <header>
      <nav>
          <a href="index.html" class="logo">GreenScapes</a>
          <ul>
              <li><a href="#parque">Parque</a></li>
              <li><a href="#pileta">Pileta</a></li>
              <li><a href="#mantenimiento">Mantenimiento</a></li>
              <li><a href="admin.html">Administrar</a></li>
          </ul>
      </nav>
  </header>

  <main>

  <section class="inicio_section">
      <h1>Green<span>Scapes</span></h1>
      <p>Mantenimiento de parques y piletas en barrios privados.</p>
      <a href="#parque" class="btn">Ver servicios</a>
  </section>

  <section id="parque" class="servicios_section parque">
      <h2>Parque</h2>
      <p class="subtitulo">Césped, poda y todo lo verde.</p>
      <div id="lista_parque" class="grid"></div>
  </section>

  <section id="pileta" class="servicios_section pileta">
      <h2>Pileta</h2>
      <p class="subtitulo">Agua limpia y lista para disfrutar.</p>
      <div id="lista_pileta" class="grid"></div>
  </section>

  <section id="mantenimiento" class="servicios_section mantenimiento">
      <h2>Mantenimiento</h2>
      <p class="subtitulo">Nos ocupamos de los detalles de tu casa.</p>
      <div id="lista_mantenimiento" class="grid"></div>
  </section>

  </main>

  <footer>
      <p>&copy; GreenScapes · Barrios privados</p>
  </footer>

  <script src="servicios.js"></script>
  </body>
  </html>

  ```

* **Servicios por categoría**: `servicios.js` pide todos los servicios y pone cada uno en la sección de su categoría (`lista_parque`, `lista_pileta` o `lista_mantenimiento`). Así, si se agrega un servicio desde el panel, aparece solo en la sección que corresponde.

* **Panel separado**: la administración está en otra página (`admin.html`) para que el cliente de la empresa solo vea el catálogo y no los botones de editar y borrar.

* **Mensajes de error**: si la API no responde, se avisa con "No se pudo conectar con la API."; si los datos están mal (422) se avisa con "Revisá los datos..." y no se borra el formulario. Antes de borrar se pide confirmación.

* **Colores**: los colores están basados en las áreas de trabajo de la empresa. Hay verdes claros y oscuros por su relación con los parques, y celeste claro y beige por su relación con las piletas. La portada y el panel usan verde oscuro y negro; Parque usa verde clarito y blanco; Pileta, beige y celeste; y Mantenimiento, gris y blanco.

* **Colores utilizados**:
  * ``--negro: #050a07;``
  * ``--verde_oscuro: #0f3d2a;``
  * ``--verde: #2e9e5b;``
  * ``--verde_clarito: #dff3e4;``
  * ``--blanco: #ffffff;``
  * ``--beige: #f5efe1;``
  * ``--celeste: #dcf0fa;``
  * ``--azul: #2a7fa8;``
  * ``--gris_claro: #eef0f1;``
  * ``--gris: #6b7479;``

* **Celular**: con un `@media (max-width: 768px)` la página se acomoda a pantallas chicas.
### ``Desarrollo con Ayuda de AI``
* Por un par de problemas con respecto a ``JavaScript`` en el diseño de webs dinámicas, se optó por utilizar inteligencia artificial para facilitar y resolver este apartado. La usé para armar los archivos `servicios.js` y `admin.js`, y después los revisé y los fui entendiendo parte por parte para poder explicarlos.

* **Qué hace `servicios.js`** (página pública):
  * Define la dirección de la API: si la página está en Netlify usa la API de Render, y si no, usa la API local (`127.0.0.1:8000`).
  * Con `fetch` hace un `GET /ver_servicios` y recibe la lista de servicios en JSON.
  * Recorre la lista con `forEach` y mete cada servicio en la sección de su categoría (`lista_parque`, `lista_pileta` o `lista_mantenimiento`) usando `innerHTML`.
  * Muestra el precio con formato argentino con `toLocaleString("es-AR")`.
  * Si la API no responde, el `.catch()` muestra un aviso.

* **Qué hace `admin.js`** (panel de administración):
  * `cargar()`: pide los servicios a la API y arma las filas de la tabla, cada una con sus botones de **Editar** y **Borrar**.
  * `guardar(event)`: frena la recarga del formulario con `preventDefault()`, junta los datos de los campos y los manda con `fetch`. Si el formulario tiene un `id` cargado, usa `PUT` para editar; si no, usa `POST` para crear. Los datos viajan como texto JSON con `JSON.stringify`.
  * `editar(id)`: busca el servicio en la lista y completa el formulario con sus datos para poder modificarlo.
  * `borrar(id)`: pide confirmación con `confirm()` y después manda un `DELETE` a la API.
  * `limpiar()`: vacía el formulario y lo deja otra vez en modo "Agregar servicio".
  * `mostrar(texto)`: muestra en pantalla los mensajes que devuelve la API o los mensajes de error.

* **Lo que aprendí con esto**: cómo usar `fetch` con los distintos métodos HTTP (`GET`, `POST`, `PUT`, `DELETE`), cómo mandar y leer JSON (`JSON.stringify` y `res.json()`), cómo usar `.then()` y `.catch()` para esperar la respuesta y manejar errores, y cómo modificar el HTML desde JavaScript con `getElementById` e `innerHTML`.

* **Catálogo inicial de servicios**: también usé IA para cargar los primeros servicios de la base de datos. Generó 25 servicios divididos en las tres categorías:
  * **Parque (10)**: corte de pasto chico, mediano y grande, poda de árboles, poda de cercos y arbustos, desmalezado, colocación de césped en panes, fertilización, control de plagas y retiro de ramas.
  * **Pileta (7)**: limpieza, mantenimiento mensual, recuperación de agua verde, vaciado y lavado, puesta a punto de temporada, cambio de arena del filtro y cobertor de invierno.
  * **Mantenimiento (8)**: limpieza de canaletas, hidrolavado de patios y veredas, pintura de rejas y portones, tratamiento de deck de madera, reparación e instalación de riego automático, luces de jardín y mantenimiento general mensual.

  Los nombres y las descripciones están basados en los trabajos que hace la empresa, pero los **precios son de referencia**, no son los precios reales de GreenScapes. Los servicios quedaron guardados en `backend/database/db.db`, y se pueden modificar o borrar desde el panel de administración.


### ``Backend``
* Separé el backend en carpetas (`models`, `managers`, `database`) para que cada archivo tenga una sola responsabilidad (ver Pregunta 5).
* La ruta a `db.db` está armada con `os.path.dirname(__file__)`, así la API siempre usa la misma base sin importar desde qué carpeta se ejecute.
* `init_db()` crea la tabla `servicios` si no existe, así la API funciona aunque la base esté vacía.
* En CORS solo permito los orígenes que uso (la página de Netlify, Live Server y `"null"` para cuando se abre con doble clic), en vez de permitir cualquier origen con `"*"`.

---

## Tecnologías usadas

| Tecnología | Para qué la usé |
|---|---|
| **Python** | Lenguaje del backend |
| **FastAPI** | Framework para armar la API y las rutas |
| **Uvicorn** | Servidor que ejecuta la API |
| **Pydantic** | Validar los datos que llegan en el body |
| **SQLite** (`sqlite3`) | Base de datos donde se guardan los servicios |
| **HTML** | Estructura de las páginas |
| **CSS** | Estilos, colores y diseño para celular |
| **JavaScript** (sin frameworks) | `fetch` para hablar con la API y armar el HTML con los datos |
| **Git y GitHub** | Control de versiones |
| **Netlify** | Publicar el frontend |
| **Render** | Publicar la API |
| **Excalidraw** | Diagramas |
