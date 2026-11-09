# =============================================================
# TP FINAL - Ejercicio 1
# Sanitización y Análisis Estadístico de Sensores
# =============================================================

# Valor seguro que se usa cuando un sensor no trae ubicación
UBICACION_POR_DEFECTO = "Sin ubicación"


# -------------------------------------------------------------
# Punto A: Normalización de lecturas
# -------------------------------------------------------------
def limpiar_registro_sensor(registro_raw):
    """Recibe un diccionario con datos crudos de un sensor
    y devuelve un diccionario nuevo con los datos limpios."""

    # 1) ID: lo pasamos a texto y le sacamos los espacios de los costados
    sensor_id = str(registro_raw.get("sensor_id", "")).strip()

    # 2) Temperatura: viene como texto, por ejemplo "24.5C" o " 26,1 °C "
    temperatura_texto = str(registro_raw.get("temperatura", "")).strip()
    temperatura_texto = temperatura_texto.upper()          # "24.5c" -> "24.5C"
    temperatura_texto = temperatura_texto.replace("°", "")  # saca el símbolo de grado
    temperatura_texto = temperatura_texto.replace("C", "")  # saca la unidad
    temperatura_texto = temperatura_texto.replace(",", ".") # coma decimal -> punto
    temperatura_texto = temperatura_texto.strip()           # saca espacios que quedaron
    temperatura = float(temperatura_texto)                  # texto -> número decimal

    # 3) Ubicación: si no viene o viene vacía, usamos el valor por defecto
    ubicacion = registro_raw.get("ubicacion")
    if ubicacion is None or str(ubicacion).strip() == "":
        ubicacion = UBICACION_POR_DEFECTO
    else:
        ubicacion = str(ubicacion).strip()

    # 4) Devolvemos un diccionario NUEVO (no modificamos el original)
    registro_limpio = {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicacion": ubicacion,
    }
    return registro_limpio


# -------------------------------------------------------------
# Punto B: Monitoreo y mapeo estadístico
# -------------------------------------------------------------
def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    """Recibe la lista de sensores ya limpios y un umbral.
    Devuelve una tupla: (IDs que superan el umbral, promedio de temperatura)."""

    lista_sensores_alerta = []  # acá guardamos los IDs en alerta
    suma_temperaturas = 0.0     # acumulador para calcular el promedio

    for sensor in lista_sensores_limpios:
        suma_temperaturas = suma_temperaturas + sensor["temperatura"]

        # "Superar" el umbral = ser estrictamente mayor
        if sensor["temperatura"] > umbral_temperatura:
            lista_sensores_alerta.append(sensor["sensor_id"])

    # Evitamos dividir por cero si la lista viene vacía
    if len(lista_sensores_limpios) > 0:
        promedio_temperatura = suma_temperaturas / len(lista_sensores_limpios)
    else:
        promedio_temperatura = 0.0

    return (lista_sensores_alerta, promedio_temperatura)


# -------------------------------------------------------------
# Bloque de ejecución: flujo completo
# -------------------------------------------------------------
if __name__ == "__main__":

    # 1) Datos crudos, tal como llegan de los microcontroladores
    registros_crudos = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002  ", "temperatura": " 31.2 °C", "ubicacion": "Planta Sur"},
        {"sensor_id": "  SENSOR-003", "temperatura": "27,8C"},  # sin ubicación
        {"sensor_id": "SENSOR-004", "temperatura": "19.0c", "ubicacion": "   "},  # ubicación vacía
        {"sensor_id": " SENSOR-005 ", "temperatura": "29.4C", "ubicacion": "Planta Este"},
    ]

    # 2) Limpiamos cada registro con la función del Punto A
    sensores_limpios = []
    for registro in registros_crudos:
        sensores_limpios.append(limpiar_registro_sensor(registro))

    print("=== REGISTROS NORMALIZADOS ===")
    for sensor in sensores_limpios:
        print(f"{sensor['sensor_id']:<12} | {sensor['temperatura']:>6.1f} °C | {sensor['ubicacion']}")

    # 3) Generamos el resumen con la función del Punto B
    umbral = 28.0
    sensores_alerta, promedio = generar_resumen_sensores(sensores_limpios, umbral)

    # 4) Imprimimos el reporte final
    print()
    print("=== REPORTE CONSOLIDADO - ECOTECH SOLUTIONS ===")
    print(f"Sensores analizados:     {len(sensores_limpios)}")
    print(f"Umbral de alerta:        {umbral:.1f} °C")
    print(f"Promedio de la planta:   {promedio:.2f} °C")
    print(f"Sensores en alerta ({len(sensores_alerta)}): {', '.join(sensores_alerta)}")
    