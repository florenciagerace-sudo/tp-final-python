# =============================================================
# TP FINAL - Ejercicio 3
# Lógica de negocio: cálculo de emisiones y métricas
# =============================================================


def calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4):
    """Calcula las emisiones de CO2 (en kg) a partir del consumo eléctrico.
    Lanza ValueError si el consumo es negativo."""
    if consumo_kwh < 0:
        raise ValueError(f"El consumo no puede ser negativo (valor recibido: {consumo_kwh}).")
    return consumo_kwh * factor_emision


def obtener_metricas_consumo(registros):
    """Procesa un historial de consumos por planta.
    Cada registro es un diccionario: {"planta": "...", "consumo_kwh": numero}.
    Devuelve un diccionario con el total de emisiones y la planta de mayor consumo."""

    consumo_por_planta = {}   # {"Planta Norte": 2700, ...}
    emisiones_por_planta = {} # {"Planta Norte": 1080.0, ...}
    total_emisiones = 0.0

    for registro in registros:
        planta = registro["planta"]
        consumo = registro["consumo_kwh"]

        # Reutilizamos la función auditada con los tests
        emisiones = calcular_emisiones_carbono(consumo)

        # Acumulamos por planta (si la planta no existe todavía, arranca en 0)
        consumo_por_planta[planta] = consumo_por_planta.get(planta, 0) + consumo
        emisiones_por_planta[planta] = emisiones_por_planta.get(planta, 0) + emisiones
        total_emisiones = total_emisiones + emisiones

    # Planta de mayor consumo (si no hay registros, queda en None)
    if consumo_por_planta:
        planta_mayor_consumo = max(consumo_por_planta, key=consumo_por_planta.get)
    else:
        planta_mayor_consumo = None

    # Detalle por planta, útil para mostrar una tabla en la web
    detalle_plantas = []
    for planta in consumo_por_planta:
        detalle_plantas.append({
            "planta": planta,
            "consumo_kwh": consumo_por_planta[planta],
            "emisiones_kg": round(emisiones_por_planta[planta], 2),
        })

    return {
        "total_emisiones": round(total_emisiones, 2),
        "planta_mayor_consumo": planta_mayor_consumo,
        "consumo_planta_mayor": consumo_por_planta.get(planta_mayor_consumo, 0),
        "detalle_plantas": detalle_plantas,
    }