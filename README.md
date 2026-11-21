# Proyecto 16 - Despliegue cloud de servidor MCP de seguros de vehículos

## Descripción

Despliegue de un servidor MCP desarrollado en Python para consultar las coberturas de pólizas de seguros de vehículos.

El proyecto parte del servidor MCP desarrollado en el Proyecto 15 y lo adapta para su ejecución mediante HTTP y Docker, preparando su despliegue en la nube.

## Herramienta disponible

### consultar_cobertura

Consulta las coberturas contratadas de una póliza de automóvil.

**Parámetro:**
- `numero_poliza`: identificador con formato AUTO-XXXX.

**Información devuelta:**
- Producto.
- Coberturas.
- Franquicia.

Las pólizas de prueba son ficticias.

## Tecnologías

- Python 3.14
- MCP SDK
- uv
- Docker
- Dockerfile
- Transporte HTTP (Streamable HTTP)
- Render (despliegue cloud)

## Endpoint de comprobación

El servidor incorpora el endpoint:

`GET /salud`

Devuelve el estado del servidor y las herramientas disponibles.

## Ejecución local

Instalar dependencias:

```powershell
py -m uv sync
```

Ejecutar mediante HTTP:

```powershell
$env:MCP_TRANSPORT="http"
py -m uv run python server.py
```

El servidor escucha en el puerto 8000 por defecto.

## Ejecución con Docker

Construir la imagen:

```powershell
docker build -t mcp-seguros-proyecto16 .
```

Arrancar el contenedor:

```powershell
docker run -d --name mcp-seguros-p16 -p 8000:8000 mcp-seguros-proyecto16
```

Comprobar el endpoint:

```powershell
Invoke-RestMethod http://localhost:8000/salud
```

Consultar los registros:

```powershell
docker logs mcp-seguros-p16
```

## Evidencias

La carpeta `evidencias/` contiene capturas de las pruebas de funcionamiento HTTP y Docker, así como de la construcción y ejecución del contenedor.

## Datos de prueba

Las pólizas utilizadas son ficticias y están definidas en `server.py`.
