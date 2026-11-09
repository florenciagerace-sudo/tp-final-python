# TP Final – Programación con Python 2026

**Alumna:** Florencia Gerace
**Caso:** EcoTech Solutions

## Estructura

```
ejercicio_1/   Sanitización y análisis estadístico de sensores
ejercicio_2/   Modelo de productos, excepciones y persistencia en JSON
ejercicio_3/   Tests unitarios + proyecto Django (panel de sustentabilidad)
```

## Ejercicio 1

```
cd ejercicio_1
python sensores.py
```

## Ejercicio 2

```
cd ejercicio_2
python catalogo.py
```

Genera el archivo `catalogo_ecotech.json` en la misma carpeta.

## Ejercicio 3

```
cd ejercicio_3
pip install -r requirements.txt
python manage.py migrate
python manage.py test sustentabilidad
python manage.py runserver
```

Luego abrir http://127.0.0.1:8000/ en el navegador.

- Tests (`TestCalculoEmisiones`): `sustentabilidad/tests.py`
- Funciones `calcular_emisiones_carbono` y `obtener_metricas_consumo`: `sustentabilidad/emisiones.py`
- Vista `vista_panel_sustentabilidad`: `sustentabilidad/views.py`
- Plantilla: `sustentabilidad/templates/sustentabilidad/panel.html`
