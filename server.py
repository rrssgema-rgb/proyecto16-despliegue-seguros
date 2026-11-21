
"""
Servidor MCP de consulta de coberturas de seguros.
Proyecto 16 - Despliegue cloud.
"""

import logging
import os
import re
import sys

from mcp.server.mcpserver import MCPServer
from starlette.requests import Request
from starlette.responses import JSONResponse

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="[mcp-seguros] %(levelname)s %(message)s"
)

log = logging.getLogger("mcp-seguros")

mcp = MCPServer("mcp-seguros")


POLIZAS = {
    "AUTO-1001": {
        "producto": "Seguro de automóvil",
        "coberturas": [
            "Responsabilidad civil",
            "Rotura de lunas",
            "Asistencia en carretera"
        ],
        "franquicia": "Sin franquicia"
    },
    "AUTO-1002": {
        "producto": "Seguro de automóvil",
        "coberturas": [
            "Responsabilidad civil",
            "Robo",
            "Incendio"
        ],
        "franquicia": "Franquicia de 300 euros"
    }
}


@mcp.tool()
def consultar_cobertura(numero_poliza: str) -> str:
    """
    Consulta las coberturas de una póliza de automóvil.

    Args:
        numero_poliza: Identificador de la póliza.
        Formato esperado: AUTO-XXXX, por ejemplo AUTO-1001.
    """

    numero_poliza = numero_poliza.strip().upper()

    if not re.fullmatch(r"AUTO-\d{4}", numero_poliza):
        log.warning("Formato de póliza no válido: %s", numero_poliza)
        return (
            "Error: formato de póliza no válido. "
            "Utiliza AUTO-XXXX, por ejemplo AUTO-1001."
        )

    poliza = POLIZAS.get(numero_poliza)

    if poliza is None:
        log.warning("Póliza no encontrada: %s", numero_poliza)
        return f"No se ha encontrado la póliza {numero_poliza}."

    log.info("Consulta realizada para la póliza %s", numero_poliza)

    coberturas = "\n".join(
        f"- {cobertura}" for cobertura in poliza["coberturas"]
    )

    return (
        f"Póliza: {numero_poliza}\n"
        f"Producto: {poliza['producto']}\n"
        f"Coberturas:\n{coberturas}\n"
        f"Franquicia: {poliza['franquicia']}"
    )


@mcp.custom_route("/salud", methods=["GET"])
async def salud(request: Request) -> JSONResponse:
    """Comprueba que el servidor está funcionando."""
    return JSONResponse({
        "estado": "ok",
        "servidor": "mcp-seguros",
        "tools": ["consultar_cobertura"]
    })


if __name__ == "__main__":
    transporte = os.environ.get("MCP_TRANSPORT", "stdio")

    log.info("Iniciando servidor MCP mediante %s", transporte)

    if transporte == "http":
        mcp.run(
            "streamable-http",
            host="0.0.0.0",
            port=int(os.environ.get("PORT", "8000"))
        )
    else:
        mcp.run()
