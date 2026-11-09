# =============================================================
# TP FINAL - Ejercicio 3 - Punto A
# Auditoría del algoritmo de emisiones con unittest
# =============================================================

import unittest

from sustentabilidad.emisiones import calcular_emisiones_carbono, obtener_metricas_consumo


class TestCalculoEmisiones(unittest.TestCase):
    """Pruebas unitarias del cálculo de huella de carbono."""

    # --- Exactitud numérica con valores nominales ---

    def test_calculo_con_factor_por_defecto(self):
        # 1000 kWh x 0.4 = 400 kg de CO2
        self.assertAlmostEqual(calcular_emisiones_carbono(1000), 400.0)

    def test_calculo_con_decimales(self):
        # 250.5 kWh x 0.4 = 100.2 kg de CO2
        self.assertAlmostEqual(calcular_emisiones_carbono(250.5), 100.2)

    def test_calculo_con_factor_personalizado(self):
        # 500 kWh x 0.5 = 250 kg de CO2
        self.assertAlmostEqual(calcular_emisiones_carbono(500, factor_emision=0.5), 250.0)

    def test_consumo_cero(self):
        # Caso límite: 0 kWh es válido y no genera emisiones
        self.assertEqual(calcular_emisiones_carbono(0), 0)

    # --- Elevación de la excepción ante consumos fuera de rango ---

    def test_consumo_negativo_lanza_value_error(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-100)

    def test_consumo_negativo_decimal_lanza_value_error(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-0.5)

    # --- Prueba extra: procesamiento de métricas ---

    def test_metricas_consumo(self):
        registros = [
            {"planta": "Planta Norte", "consumo_kwh": 1000},
            {"planta": "Planta Sur", "consumo_kwh": 500},
            {"planta": "Planta Norte", "consumo_kwh": 200},
        ]
        metricas = obtener_metricas_consumo(registros)
        # Total: (1000 + 500 + 200) x 0.4 = 680 kg
        self.assertAlmostEqual(metricas["total_emisiones"], 680.0)
        # Planta Norte suma 1200 kWh, más que Planta Sur (500 kWh)
        self.assertEqual(metricas["planta_mayor_consumo"], "Planta Norte")


if __name__ == "__main__":
    unittest.main()