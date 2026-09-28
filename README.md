# GreenScapes — TP Full Stack

**Nombre y apellido:** Enzo Benjamin Romero  
**Curso:** 6° 5°

---

## Descripción del tema

GreenScapes es una agencia ficticia de mantenimiento de parques y piletas en barrios privados.

La app tiene:

- Una página pública (`index.html`) con los servicios separados en **Parque, Pileta y Mantenimiento**.
- Un panel de administración (`admin.html`) para **agregar, editar y borrar** servicios.
- Una API hecha con **FastAPI** que guarda los datos en **SQLite**.

Cada servicio tiene nombre, descripción, precio y categoría.

## Tecnologías usadas

| Tecnología | Para qué se usa |
|---|---|
| Python | Backend |
| FastAPI | API y endpoints |
| Uvicorn | Ejecuta el servidor |
| Pydantic | Valida los datos |
| SQLite | Guarda los servicios |
| HTML y CSS | Página y diseño |
| JavaScript + fetch | Conecta la página con la API |

## Instalación y ejecución

Requisitos: **Python 3.10 o más nuevo** y **Git**.

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/Enzis123/full-stackiiiiiiiiiii.git
   cd full-stackiiiiiiiiiii
   ```
2. Crear y activar el entorno virtual:
   ```bash
   python -m venv env
   env\Scripts\activate            # Windows (CMD)
   .\env\Scripts\Activate.ps1      # Windows (PowerShell)
   source env/bin/activate        # Linux o Mac
   ```
3. Instalar las dependencias y levantar la API:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```
   La API queda en `http://127.0.0.1:8000` y la documentación en `http://127.0.0.1:8000/docs`.
4. Con la API corriendo, abrir `greenscapes/index.html` (catálogo) o `greenscapes/admin.html` (administración) en el navegador, con doble clic o con la extensión Live Server de VS Code.

---

## Endpoints

| Operación | Método | Ruta | Qué hace |
|---|---|---|---|
| Crear | POST | `/agregar_servicios` | Crea un servicio |
| Listar | GET | `/ver_servicios` | Muestra todos |
| Buscar uno | GET | `/ver_servicio/{id}` | Busca por id |
| Editar | PUT | `/editar_servicio/{id}` | Edita un servicio |
| Borrar | DELETE | `/borrar_servicio/{id}` | Borra un servicio |

### Códigos importantes

- **200:** salió bien.
- **201:** sería el código correcto al crear, aunque actualmente la API devuelve 200.
- **404:** no encontrado. Actualmente la API no lo usa para un id inexistente.
- **422:** los datos enviados no cumplen el modelo de Pydantic.
- **500:** error interno del servidor.

### Ejemplos de request y response

**Listar servicios**
```http
GET /ver_servicios
```
```json
[
  {"id": 5, "servicio": "Corte de pasto chico", "descripcion": "Corte de pasto hasta 100m2, incluye bordeado y retiro de restos", "precio": 60000.0, "categoria": "Parque"},
  {"id": 15, "servicio": "Limpieza de pileta", "descripcion": "Barrido de fondo, limpieza de paredes y línea de flote, aspirado y control de cloro", "precio": 55000.0, "categoria": "Pileta"}
]
```

**Buscar un servicio**
```http
GET /ver_servicio/5
```
```json
{"id": 5, "servicio": "Corte de pasto chico", "descripcion": "Corte de pasto hasta 100m2, incluye bordeado y retiro de restos", "precio": 60000.0, "categoria": "Parque"}
```
Si el id no existe:
```json
{"mensaje": "No existe un servicio con ese id"}
```

**Crear un servicio**
```http
POST /agregar_servicios
Content-Type: application/json

{"servicio": "Limpieza de filtro", "descripcion": "Limpieza del filtro de la pileta", "precio": 30000, "categoria": "Pileta"}
```
```json
{"mensaje": "Servicio agregado"}
```

**Editar un servicio**
```http
PUT /editar_servicio/31
Content-Type: application/json

{"servicio": "Limpieza de filtro", "descripcion": "Limpieza del filtro de la pileta", "precio": 35000, "categoria": "Pileta"}
```
```json
{"mensaje": "Servicio editado"}
```

**Borrar un servicio**
```http
DELETE /borrar_servicio/31
```
```json
{"mensaje": "Servicio borrado"}
```

**Request inválido** (falta `descripcion` y `categoria`, y el precio no es un número)
```http
POST /agregar_servicios
Content-Type: application/json

{"servicio": "Poda", "precio": "mucho"}
```
Respuesta con código **422**:
```json
{
  "detail": [
    {"type": "missing", "loc": ["body", "descripcion"], "msg": "Field required"},
    {"type": "float_parsing", "loc": ["body", "precio"], "msg": "Input should be a valid number, unable to parse string as a number"},
    {"type": "missing", "loc": ["body", "categoria"], "msg": "Field required"}
  ]
}
```

---

## Capturas de pantalla

**Inicio**
![Inicio](docs/capturas/inicio.png)

**Catálogo de servicios**
![Servicios](docs/capturas/servicios.png)

**Panel de administración**
![Administrar](docs/capturas/admin.png)

**Vista en celular**

<img src="docs/capturas/celular.png" alt="Vista en celular" width="300">

---

## Criterios de diseño

- **Dos páginas separadas:** el catálogo (`index.html`) solo muestra servicios y la administración (`admin.html`) tiene agregar, editar y borrar. Así el que mira los servicios no ve los botones de administración.
- **Colores por categoría:** Parque en verde clarito y blanco, Pileta en beige claro y celeste claro, Mantenimiento en gris y blanco. La portada y el panel de administración usan verde oscuro con negro.
- **HTML, CSS y JavaScript sin frameworks**, para que el código sea simple y fácil de entender.
- **Backend separado en capas:** `database/` (conexión), `models/` (modelo de datos), `managers/` (consultas a la base) y `main.py` (endpoints).
- **SQLite** como base de datos, porque es un solo archivo y no hace falta instalar un servidor de base de datos.

---

## Preguntas de arquitectura cliente-servidor

### Pregunta 1 — El ciclo de vida de una petición

Cuando toco **Guardar** en `admin.html` pasa esto:

1. `guardar()` toma los datos del formulario.
2. `event.preventDefault()` evita que se recargue la página.
3. JavaScript arma el objeto `datos`.
4. `fetch()` manda un **POST** a `/agregar_servicios` y `JSON.stringify()` convierte los datos a JSON.
5. Uvicorn recibe el pedido y FastAPI busca la función correspondiente.
6. **Pydantic** revisa los datos. Si falta algo o el precio no es un número, devuelve **422** y no toca la base.
7. `Depends(get_db)` abre la conexión a SQLite.
8. `manager.crear()` hace el `INSERT` y `commit()`. Ahí se guarda realmente el dato.
9. La API devuelve `{"mensaje": "Servicio agregado"}` con código 200.
10. Se cierra la conexión.
11. `admin.js` recibe la respuesta, muestra el mensaje, limpia el formulario y hace otro `GET /ver_servicios` para actualizar la tabla.

**En resumen:** `admin.js → FastAPI → Pydantic → get_db → manager → SQLite → respuesta → actualizar tabla`.

![Gráfico del ciclo de una petición](docs/graficos/solicitud-guardar.png)

---

### Pregunta 2 — ¿Quién es el cliente y quién es el servidor?

El **cliente** es el navegador, que ejecuta el HTML, CSS y JavaScript de `greenscapes/`.

El **servidor** es FastAPI, que corre con Uvicorn en el puerto `8000`.

El navegador y la API se comunican por **HTTP** y mandan los datos en **JSON**.

La base `db.db` está del lado del servidor. El navegador nunca entra directamente a SQLite.

A diferencia de una app de escritorio, acá la interfaz y los datos están separados. Los datos están centralizados en el servidor.

![Gráfico de arquitectura cliente-servidor](docs/graficos/arquitectura.png)

---

### Pregunta 3 — HTTP como lenguaje común

**HTTP** es el conjunto de reglas que usa el navegador para comunicarse con la API.

Un pedido tiene principalmente:

- **Método:** GET, POST, PUT o DELETE.
- **Ruta:** por ejemplo `/ver_servicios`.
- **Headers:** información extra, como `Content-Type: application/json`.
- **Body:** los datos enviados, principalmente en POST y PUT.

La respuesta tiene un código de estado y un body, que en este proyecto es JSON.

#### Tabla de la API

| Operación | Método | Ruta | Código de éxito | Código de error |
|---|---|---|---|---|
| Crear | POST | `/agregar_servicios` | 200 | 422 |
| Listar | GET | `/ver_servicios` | 200 + lista JSON | — |
| Buscar uno | GET | `/ver_servicio/{id}` | 200 + servicio | 422 si el id no es entero |
| Editar | PUT | `/editar_servicio/{id}` | 200 | 422 |
| Borrar | DELETE | `/borrar_servicio/{id}` | 200 | 422 |

Un detalle: si el id es un número pero no existe, actualmente la API devuelve 200. Lo ideal sería devolver 404.

---

### Pregunta 4 — CORS

CORS sirve para que el navegador pueda aceptar respuestas de una API que está en otro origen.

Un origen está formado por:

**protocolo + dominio + puerto**

Por ejemplo:

- Frontend: `http://127.0.0.1:5500`
- API: `http://127.0.0.1:8000`

Como cambia el puerto, son orígenes distintos.

En `main.py` se usa `CORSMiddleware` con:

```python
allow_origins=["*"]
allow_methods=["*"]
allow_headers=["*"]
```

Eso permite que cualquier origen pueda usar la API. Para producción sería mejor poner solamente el dominio necesario.

En pedidos como POST, PUT o DELETE, el navegador puede hacer primero un **OPTIONS**, llamado preflight, para preguntar si tiene permiso. Después manda el pedido real.

Importante: **CORS no protege la API contra Postman, curl o scripts**. Es una regla que aplica el navegador.

![Gráfico del flujo CORS](docs/graficos/cors.png)

---

### Pregunta 5 — Separación de responsabilidades

Cada parte del backend tiene una función:

| Archivo | Qué hace |
|---|---|
| `main.py` | Rutas y respuestas HTTP |
| `manager.py` | Consultas SQL |
| `database_conn.py` | Abre y cierra la conexión |
| `modelServicios.py` | Define y valida cómo es un servicio |

La idea es no mezclar todo en un solo archivo.

Por ejemplo, `main.py` recibe el pedido, pero no hace directamente el SQL. El manager se encarga de eso.

#### ¿Qué hace `Depends(get_db)`?

Le dice a FastAPI que antes de ejecutar la ruta tiene que llamar a `get_db()` y pasarle la conexión.

`get_db()` abre la conexión, la presta con `yield` y después la cierra en `finally`.

Así cada pedido usa su conexión y esta se cierra aunque haya un error.

---

### Pregunta 6 — JSON como formato de intercambio

**JSON** es un formato de texto con claves y valores que sirve para pasar datos entre el navegador y la API.

Ejemplo:

```json
{
  "id": 5,
  "servicio": "Corte de pasto chico",
  "descripcion": "Corte de pasto hasta 100m2",
  "precio": 60000.0,
  "categoria": "Parque"
}
```

JavaScript y Python pueden trabajar fácilmente con JSON.

En el frontend:

```javascript
JSON.stringify(datos)
```

convierte el objeto de JavaScript en texto JSON para enviarlo.

Y:

```javascript
res.json()
```

convierte la respuesta JSON en un objeto que JavaScript puede usar.

Si los datos no cumplen el modelo de Pydantic, la API devuelve **422** y no guarda nada.

---

### Pregunta 7 — Statelessness (sin estado)

**Stateless** significa que el servidor no depende de recordar las peticiones anteriores.

Cada pedido tiene que traer la información necesaria para poder responder.

En GreenScapes, los servicios no quedan guardados en la memoria de FastAPI. Los datos están en SQLite.

Además, `get_db()` abre una conexión para la petición y la cierra al terminar.

Por eso, si se reinicia Uvicorn, los servicios siguen estando en `db.db`.

Si el proyecto creciera y tuviera varios servidores, todos podrían atender pedidos porque la API no depende de datos guardados en la memoria de un servidor. Para hacerlo realmente con varios servidores habría que usar una base compartida, como PostgreSQL o MySQL, porque SQLite es un archivo local.

---

## Glosario rápido

- **API:** programa que permite que otros programas hagan pedidos y reciban datos.
- **Endpoint:** una ruta de la API.
- **HTTP:** reglas para comunicarse entre cliente y servidor.
- **JSON:** formato para intercambiar datos.
- **CORS:** permiso para que el navegador pueda leer respuestas de otro origen.
- **Pydantic:** valida los datos.
- **FastAPI:** framework usado para crear la API.
- **Uvicorn:** ejecuta el servidor.
- **SQLite:** base de datos guardada en un archivo.
- **CRUD:** crear, leer, actualizar y borrar.
- **fetch:** función de JavaScript para hacer pedidos HTTP.
- **Stateless:** el servidor no guarda el estado de las peticiones anteriores.

