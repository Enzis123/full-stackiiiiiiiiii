# GreenScapes — TP Full Stack

**Nombre y apellido:** _completar_  
**Curso:** _completar_

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

Requisitos: Python 3.9 o más nuevo y Git.

```bash
git clone https://github.com/Enzis123/full-stackiiiiiiiiiii.git
cd full-stackiiiiiiiiiii
python -m venv env
env\Scripts\activate
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

La API queda en `http://127.0.0.1:8000` y la documentación en `http://127.0.0.1:8000/docs`.

Después abrir `greenscapes/index.html` o `admin.html`.

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

---

# Preguntas de arquitectura cliente-servidor

## Pregunta 1 — El ciclo de vida de una petición

Cuando completo el formulario de `admin.html` y toco **Guardar**, pasa esto paso a paso:

1. El formulario tiene `onsubmit="guardar(event)"`, así que se ejecuta `guardar()`.
2. `event.preventDefault()` evita que el formulario haga su envío normal y recargue la página.
3. JavaScript arma el objeto `datos` con lo que escribió el usuario. El precio pasa por `Number()` para que viaje como número.
4. Como el campo `id` está vacío, es un alta, entonces se usa `POST /agregar_servicios`. Si hubiera un id, se usaría `PUT /editar_servicio/{id}`.
5. `fetch()` manda el pedido. `JSON.stringify(datos)` convierte el objeto de JavaScript en texto JSON y `Content-Type: application/json` avisa que el body es JSON.
6. Uvicorn recibe el pedido y FastAPI busca la función que corresponde a `POST /agregar_servicios`: `agregar_servicio()`.
7. Pydantic valida el JSON contra `modelServicios`. Revisa que estén los cuatro campos y que `precio` sea un número. Si algo está mal, FastAPI devuelve **422**, la función no se ejecuta y la base no se toca.
8. Si todo está bien, `Depends(db_conn.get_db)` hace que FastAPI abra una conexión a SQLite y se la pase a la ruta.
9. `manager.crear()` hace el `INSERT` y después `commit()`. Recién con el `commit()` el dato queda guardado en `db.db`.
10. La función devuelve `{"mensaje": "Servicio agregado"}` y FastAPI responde con código **200** y JSON.
11. Cuando termina la petición, el `finally` de `get_db()` ejecuta `conn.close()` y cierra la conexión.
12. En el navegador, `res.json()` convierte la respuesta en un objeto. Después `mostrar()` muestra el mensaje y `limpiar()` vacía el formulario.
13. `cargar()` hace un **segundo pedido**, esta vez `GET /ver_servicios`, para traer la lista actualizada.
14. La API vuelve a abrir una conexión, `manager.listar()` hace un `SELECT` y devuelve la lista en JSON.
15. JavaScript recibe la lista y vuelve a dibujar la tabla, mostrando también el servicio nuevo.

O sea, hay **dos viajes**: primero un POST para guardar y después un GET para traer la lista actualizada.

**En resumen:** `clic en Guardar → guardar() → fetch POST → FastAPI → Pydantic → get_db → manager.crear → INSERT + commit → SQLite → respuesta JSON → res.json() → cargar() → GET /ver_servicios → tabla actualizada`.

![Gráfico del ciclo de una petición](docs/graficos/solicitud-guardar.png)

---
## Pregunta 2 — ¿Quién es el cliente y quién es el servidor?

El **cliente** es el navegador. Es el programa que ejecuta el HTML, CSS y JavaScript de `greenscapes/` y desde ahí hace los `fetch()` para pedir o modificar datos.

El **servidor** es la API de FastAPI que corre con Uvicorn en el puerto `8000`. Recibe los pedidos, ejecuta las rutas y es el único que accede directamente a SQLite.

La base `db.db` está del lado del servidor. El navegador nunca abre directamente el archivo SQLite.

El cliente y el servidor se comunican por **HTTP**, usando GET, POST, PUT y DELETE, e intercambian los datos en **JSON**.

### Diferencia con una aplicación de escritorio

En una aplicación de escritorio tradicional, la interfaz, la lógica y normalmente los datos están dentro del mismo programa y en una misma PC.

En GreenScapes están separados:

| | Aplicación de escritorio | GreenScapes cliente-servidor |
|---|---|---|
| Interfaz | Programa instalado | Navegador |
| Lógica | En el mismo programa | FastAPI en el servidor |
| Datos | Generalmente en la PC | SQLite del lado del servidor |
| Usuarios | Cada instalación puede tener sus datos | Varios clientes pueden usar el mismo servidor |
| Actualización | Hay que actualizar/reinstalar el programa | Se actualiza el servidor |
| Comunicación | Puede funcionar sin red si todo es local | Cliente y servidor se comunican por HTTP |

Por ejemplo, si desde `admin.html` agrego un servicio, después alguien que abra `index.html` puede verlo porque las dos páginas consultan la misma API y la misma base.

![Gráfico de arquitectura cliente-servidor](docs/graficos/arquitectura.png)

---
## Pregunta 3 — HTTP como lenguaje común

**HTTP** es el conjunto de reglas que usa el navegador para comunicarse con la API. Es como un idioma común: el cliente hace un **request** y el servidor devuelve un **response**.

Un pedido tiene principalmente:

- **Método:** indica qué quiero hacer, como GET, POST, PUT o DELETE.
- **Ruta:** indica sobre qué recurso trabajo, por ejemplo `/ver_servicios`.
- **Headers:** información extra, como `Content-Type: application/json`.
- **Body:** los datos que se mandan. En este proyecto se usa principalmente en POST y PUT.

La respuesta tiene un **código de estado** y un **body**, que en este proyecto normalmente es JSON.

### ¿Qué hace cada método?

- **GET:** sirve para pedir o leer datos. Por ejemplo, `GET /ver_servicios` pide todos los servicios y `GET /ver_servicio/{id}` busca uno.
- **POST:** sirve para crear algo nuevo. Por ejemplo, `POST /agregar_servicios` crea un servicio.
- **PUT:** sirve para modificar o reemplazar los datos de un servicio que ya existe. Por ejemplo, `PUT /editar_servicio/{id}` usa el id de la URL y los datos nuevos del body.
- **DELETE:** sirve para borrar un servicio. Por ejemplo, `DELETE /borrar_servicio/{id}` borra el servicio indicado.

### Códigos de estado

- **200 OK:** el pedido salió bien.
- **201 Created:** salió bien y se creó algo nuevo. Sería el código indicado para crear un servicio.
- **404 Not Found:** no se encontró el recurso pedido. Nuestra API no usa este código actualmente para un id inexistente.
- **422 Unprocessable Entity:** el pedido llegó, pero los datos no cumplen lo que espera la API, por ejemplo falta un campo o el precio no se puede convertir a número.

### Tabla de la API

| Operación | Método | Ruta | Código de éxito | Código de error |
|---|---|---|---|---|
| Crear | POST | `/agregar_servicios` | **200** + `{"mensaje":"Servicio agregado"}` | **422** si el body está mal |
| Listar | GET | `/ver_servicios` | **200** + lista JSON | — |
| Buscar uno | GET | `/ver_servicio/{id}` | **200** + servicio | **422** si el id no es entero |
| Editar | PUT | `/editar_servicio/{id}` | **200** + `{"mensaje":"Servicio editado"}` | **422** si el body está mal o el id no es entero |
| Borrar | DELETE | `/borrar_servicio/{id}` | **200** + `{"mensaje":"Servicio borrado"}` | **422** si el id no es entero |

Si el id es un número pero no existe, la API actualmente responde **200**. En el GET devuelve un mensaje de que no existe, y en PUT o DELETE puede devolver el mensaje de éxito aunque no haya cambiado ninguna fila.

### ¿Por qué devuelve esos códigos nuestra API?

**Crear devuelve 200 y no 201:** FastAPI devuelve **200 por defecto** y en la ruta no se configuró `status_code=201`.

**No devuelve 404 para un id inexistente:** el manager no comprueba primero si ese id existe. Hace la operación y la ruta termina respondiendo 200. Para mejorarlo habría que comprobar si existe y devolver `HTTPException(status_code=404)` cuando no se encuentra.

**Aparece 422:** FastAPI lo devuelve automáticamente cuando Pydantic no puede validar los datos del pedido. Por ejemplo, si falta un campo o se manda texto donde debería haber un número. La función de la ruta ni siquiera llega a ejecutarse.

---
## Pregunta 4 — CORS

CORS sirve para que el navegador pueda permitir que una página lea respuestas de una API que está en otro origen.

Un **origen** está formado por:

**protocolo + dominio + puerto**

Por ejemplo:

- Frontend con Live Server: `http://127.0.0.1:5500`
- API: `http://127.0.0.1:8000`

Como cambia el puerto, son orígenes distintos. Si se abre el HTML con doble clic, el origen es `null`.

### ¿Qué es el SOP?

El **SOP (Same-Origin Policy)** es una regla de seguridad del navegador. Básicamente dice que una página solo puede leer normalmente respuestas de su mismo origen.

El objetivo es **proteger al usuario**. Por ejemplo, si alguien tiene abierta una sesión en su home banking y entra a una página maliciosa, esa página no debería poder hacer pedidos al banco usando esa sesión y después leer los datos de la respuesta.

### ¿Cómo entra CORS en esto?

CORS funciona como una excepción al SOP: el servidor puede autorizar que otros orígenes puedan leer sus respuestas.

El servidor lo indica mediante headers como `Access-Control-Allow-Origin`. En GreenScapes usamos `CORSMiddleware` de FastAPI para agregar esos headers.

En el `main.py` se usa:

```python
origenes_permitidos = [
    "https://greenscapesproyect.netlify.app",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "null",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origenes_permitidos,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)
```

Así esas páginas tienen permitido leer las respuestas de la API desde el navegador.

### ¿Qué pasa con el preflight?

En pedidos como un **POST con JSON**, un **PUT** o un **DELETE**, el navegador puede hacer primero un pedido `OPTIONS`, llamado **preflight**.

El navegador pregunta si el origen tiene permiso y qué métodos y headers están permitidos. Si la respuesta indica que está permitido, recién después manda el pedido real, por ejemplo `POST /agregar_servicios`.

El flujo sería:

`Navegador → OPTIONS /agregar_servicios → FastAPI → respuesta CORS → Navegador → POST /agregar_servicios → FastAPI → respuesta JSON`

Importante: **CORS es una regla del navegador, no una protección completa de la API**. Postman, `curl` o un script de Python no dependen de CORS y pueden llamar directamente a la API.

![Gráfico del flujo CORS](docs/graficos/cors.png)

---
## Pregunta 5 — Separación de responsabilidades

En el backend cada parte tiene una función distinta:

| Archivo | Qué hace |
|---|---|
| `main.py` | Define las rutas y las respuestas HTTP. No hace directamente el SQL. |
| `manager.py` | Hace las consultas SQL: listar, crear, buscar, editar y borrar. |
| `database_conn.py` | Abre y cierra la conexión y crea la tabla al iniciar. |
| `modelServicios.py` | Define cómo tiene que ser un servicio y valida sus datos. |

La idea es separar responsabilidades para que cada archivo haga un solo trabajo.

### ¿Qué beneficios tiene separar el Manager de los endpoints?

- Si cambiamos SQLite por otra base, como PostgreSQL, principalmente tenemos que cambiar el manager y la conexión, sin modificar todas las rutas de `main.py`.
- Es más fácil encontrar errores. Si falla una consulta SQL, sabemos que tenemos que revisar el manager.
- Las funciones del manager se pueden reutilizar desde distintas rutas.
- El código queda más ordenado y es más fácil de entender.

Una forma de explicarlo es con un restaurante:

- **`main.py` es el mozo:** recibe el pedido y lleva la respuesta al cliente.
- **`manager.py` es el cocinero:** sabe hacer las consultas SQL y trabajar con los datos.
- **`db.db` es la heladera:** ahí están guardados los datos.

Si cambio la heladera, el mozo no necesita aprender a cocinar de nuevo.

### ¿Qué hace `Depends(get_db)`?

En las rutas aparece algo como `db=Depends(db_conn.get_db)`. Eso significa que FastAPI, antes de ejecutar la función, llama a `get_db()` y le pasa la conexión en `db`.

`get_db()` hace esto:

1. Abre la conexión.
2. Usa `yield` para prestársela a la ruta.
3. La ruta usa esa misma conexión y se la pasa al manager.
4. Cuando la ruta termina, el `finally` ejecuta `conn.close()`.

### Beneficios de la inyección de dependencias

- Hay un solo lugar encargado de abrir y cerrar la conexión.
- La conexión se cierra siempre, incluso si ocurre un error, gracias a `try/finally`.
- Si cambia el archivo o el motor de la base, se puede modificar `get_db()` sin cambiar todas las rutas.
- Para hacer pruebas se puede inyectar otra base de datos de prueba sin modificar las rutas.
- Cada pedido usa una conexión para todo lo que hace ese pedido.

### ¿Qué pasaría si abriéramos una conexión nueva por cada línea?

Sería peor por varias razones:

- Sería **más lento**, porque abrir una conexión cuesta tiempo.
- Habría **muchas conexiones abiertas** al mismo tiempo y se gastarían más recursos.
- SQLite podría tener **bloqueos**. Como la base es un solo archivo, si una conexión está escribiendo y otra quiere escribir puede aparecer `database is locked`.
- Los cambios quedarían repartidos entre distintas conexiones y sería más fácil tener problemas con los `commit()`.
- También sería fácil olvidarse de cerrar alguna conexión y generar fugas de recursos.

Por eso se usa una conexión por petición y se deja que `get_db()` se encargue de cerrarla.

---
## Pregunta 6 — JSON como formato de intercambio

**JSON** es un formato de texto que organiza los datos usando claves y valores. Sirve para que el cliente y el servidor puedan intercambiar información de una forma que los dos entienden.

Por ejemplo, un servicio puede viajar así:

```json
{
  "id": 5,
  "servicio": "Corte de pasto chico",
  "descripcion": "Corte de pasto hasta 100m2",
  "precio": 60000.0,
  "categoria": "Parque"
}
```

### ¿Por qué usamos JSON?

- Es texto, por lo que se puede enviar fácilmente por HTTP.
- Es liviano y fácil de leer.
- No depende de un lenguaje. El frontend está en JavaScript y el backend en Python, pero ambos pueden trabajar con JSON.
- Es un formato estándar usado en las APIs web.

### ¿Cómo va y vuelve el JSON?

En el frontend, `guardar()` arma un objeto de JavaScript y usa:

```javascript
JSON.stringify(datos)
```

Esto convierte el objeto en texto JSON para mandarlo en el body.

Además, el header `Content-Type: application/json` le avisa a FastAPI que el body contiene JSON.

Cuando la respuesta vuelve al navegador, se usa:

```javascript
res.json()
```

Esto convierte la respuesta JSON en un objeto que JavaScript puede usar.

### ¿Cómo procesa Pydantic los datos?

Cuando llega el JSON a FastAPI pasa esto:

1. FastAPI lee el JSON que llegó en el body.
2. Pydantic arma un objeto usando el modelo `modelServicios`.
3. Revisa que estén los cuatro campos: `servicio`, `descripcion`, `precio` y `categoria`.
4. Revisa los tipos. Por ejemplo, `precio` tiene que poder convertirse a `float`.
5. Pydantic es flexible con algunos tipos. Por ejemplo, un valor como `"30000"` puede convertirse en `30000.0`.
6. Si algo no cumple el modelo, FastAPI devuelve **422** y la función de la ruta no se ejecuta. Por eso la base no se toca.

### ¿Qué garantiza la validación?

Garantiza que al manager le lleguen los cuatro campos necesarios y que los valores tengan los tipos que pide el modelo.

Pero el modelo actual **no garantiza todo**. Por ejemplo:

- Un precio negativo puede pasar.
- Un texto vacío puede pasar.
- Se puede mandar una categoría que no sea `Parque`, `Pileta` o `Mantenimiento`.

El formulario de `admin.html` tiene algunas restricciones, pero alguien puede llamar directamente a la API, por ejemplo desde `/docs`, y saltearse esas restricciones. Por eso las validaciones importantes deberían estar también en el backend.

### Ejemplo de request inválido

Si mandamos:

```http
POST /agregar_servicios
Content-Type: application/json

{"servicio": "Poda", "precio": "mucho"}
```

FastAPI responde **422** porque falta `descripcion`, falta `categoria` y `"mucho"` no se puede convertir a número.

La respuesta es:

```json
{
  "detail": [
    {"type": "missing", "loc": ["body", "descripcion"], "msg": "Field required"},
    {"type": "float_parsing", "loc": ["body", "precio"], "msg": "Input should be a valid number, unable to parse string as a number"},
    {"type": "missing", "loc": ["body", "categoria"], "msg": "Field required"}
  ]
}
```

- **`detail`**: contiene la lista de errores encontrados.
- **`type`**: indica qué tipo de error ocurrió. `missing` significa que falta un campo y `float_parsing` que no pudo convertir el valor a número.
- **`loc`**: indica dónde está el error. Por ejemplo, `["body", "precio"]` significa que el error está en `precio`, dentro del body.
- **`msg`**: explica el error con palabras.

En este caso, **no se guarda nada en `db.db`** porque la función de la ruta no llega a ejecutarse.

---
## Pregunta 7 — Statelessness (sin estado)

HTTP es un protocolo **stateless**, que significa que el servidor no tiene que recordar las peticiones anteriores para poder responder la siguiente.

En GreenScapes, cada petición trae la información necesaria. Por ejemplo, en `PUT /editar_servicio/5`, el `5` está en la URL y los datos nuevos están en el body. El servidor no necesita recordar qué pidió el usuario antes.

En el proyecto se puede ver porque:

- No hay una lista global de servicios guardada en `main.py` para usarla entre pedidos.
- `get_db()` abre una conexión para la petición, la presta con `yield` y la cierra al terminar.
- Los datos reales viven en `backend/database/db.db`, no en la memoria de FastAPI.
- Si se reinicia Uvicorn, los servicios siguen estando en SQLite.
- En `admin.js` puede existir una copia temporal de la lista en la variable `servicios`, pero la fuente real de los datos siempre es la base. Después de guardar o borrar, se vuelve a llamar a `cargar()` para actualizarla.

### ¿Qué ventaja tendría usar 3 servidores?

Si mañana hubiera tres servidores FastAPI funcionando al mismo tiempo, un balanceador podría repartir las peticiones entre ellos.

Como ninguno guarda el estado de los servicios en su propia memoria, cualquiera de los tres podría atender una petición. Todos tendrían que leer y escribir sobre la **misma base de datos compartida**.

Esto permite escalar agregando más servidores y también hace que, si uno deja de funcionar, los otros puedan seguir atendiendo pedidos.

Pero hay una aclaración importante: **SQLite no sirve como base compartida entre tres servidores en máquinas distintas**, porque `db.db` es un archivo local. Para hacerlo de verdad habría que cambiar SQLite por una base de datos compartida, como PostgreSQL o MySQL.

La parte stateless de la API seguiría igual; lo que cambiaría sería dónde se guardan los datos.

