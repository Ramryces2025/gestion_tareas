# gestion_tareas
Pequena API de gestion de tareas en memoria usando FastAPI, con endpoints basicos para crear, listar y borrar tareas.

## Endpoints
- `GET /tasks` devuelve todas las tareas.
- `POST /tasks` crea una tarea nueva (`title`, `description` opcional).
- `DELETE /tasks/{id}` elimina la tarea con el id indicado (404 si no existe).

## Ejecutar el servicio
1) Instalar dependencias: `pip install -r requirements.txt`
2) Levantar en local con recarga: `uvicorn main:app --host 0.0.0.0 --port 8005 --reload`
3) Documentacion interactiva (Swagger): `http://localhost:8005/docs`

### Docker (hot reload montando el codigo)
- `docker build -t gestion_tareas .`
- En Windows PowerShell: `docker run --name gestion_app -p 8005:8000 -v "${PWD}:/app" gestion_tareas`
- En Linux/macOS: `docker run --name gestion_app -p 8005:8005 -v "$(pwd):/app" gestion_tareas`

## Pruebas
Ejecutar `python -m pytest -q` para correr la suite automatizada.
