# =============================================================
# TP FINAL - Ejercicio 3 - Punto B
# Vista de Django para el panel de sustentabilidad
# =============================================================

from django.shortcuts import render

from .emisiones import obtener_metricas_consumo

# Historial de consumos por planta industrial (datos de ejemplo)
HISTORIAL_CONSUMOS = [
    {"planta": "Planta Norte", "consumo_kwh": 12500},
    {"planta": "Planta Sur", "consumo_kwh": 8300},
    {"planta": "Planta Este", "consumo_kwh": 15200},
    {"planta": "Planta Norte", "consumo_kwh": 11800},
    {"planta": "Planta Sur", "consumo_kwh": 9100},
    {"planta": "Planta Este", "consumo_kwh": 14700},
]


def vista_panel_sustentabilidad(request):
    """Procesa el historial de consumos y envía los resultados a la plantilla."""

    # 1) Procesamos los datos con la lógica de negocio
    metricas = obtener_metricas_consumo(HISTORIAL_CONSUMOS)

    # 2) Armamos el diccionario de contexto para la plantilla
    contexto = {
        "titulo": "Panel de Sustentabilidad - EcoTech Solutions",
        "total_emisiones": metricas["total_emisiones"],
        "planta_mayor_consumo": metricas["planta_mayor_consumo"],
        "consumo_planta_mayor": metricas["consumo_planta_mayor"],
        "detalle_plantas": metricas["detalle_plantas"],
    }

    # 3) Renderizamos la plantilla con el contexto
    return render(request, "sustentabilidad/panel.html", contexto)