# =============================================================
# TP FINAL - Ejercicio 2
# Modelo de Productos, Excepciones y Persistencia
# =============================================================

import json  # librería estándar para trabajar con archivos JSON
import os    # librería estándar para armar rutas de archivos


# -------------------------------------------------------------
# Punto A: Dominio del catálogo y reglas de inventario
# -------------------------------------------------------------

class StockInvalidoError(Exception):
    """Excepción de negocio: se lanza cuando se intenta
    asignar un stock negativo a un dispositivo."""
    pass


class DispositivoEcológico:
    """Clase base para todos los productos ecológicos del catálogo."""

    def __init__(self, codigo, nombre, precio, stock):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        # Usamos el setter (más abajo) para que el stock se valide
        # también al crear el objeto
        self.stock = stock

    # --- Encapsulamiento del stock ---
    # El valor real se guarda en self.__stock (atributo privado).
    # Desde afuera solo se puede leer o cambiar a través de la propiedad.

    @property
    def stock(self):
        """Getter: devuelve el stock actual."""
        return self.__stock

    @stock.setter
    def stock(self, nuevo_stock):
        """Setter: valida el valor antes de guardarlo."""
        if nuevo_stock < 0:
            raise StockInvalidoError(
                f"El stock de '{self.nombre}' no puede ser negativo (valor recibido: {nuevo_stock})."
            )
        self.__stock = nuevo_stock

    def ficha_tecnica(self):
        """Devuelve la ficha comercial del producto como texto."""
        return (
            f"[{self.codigo}] {self.nombre}\n"
            f"  Precio: ${self.precio:,.2f}\n"
            f"  Stock disponible: {self.stock} unidades"
        )

    def to_dict(self):
        """Convierte el objeto en un diccionario para poder guardarlo en JSON."""
        return {
            "tipo": "DispositivoEcológico",
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
        }


class PanelSolar(DispositivoEcológico):
    """Clase especializada: hereda todo de DispositivoEcológico
    y agrega atributos propios de un panel solar."""

    def __init__(self, codigo, nombre, precio, stock, potencia_watts, eficiencia):
        # super() llama al __init__ de la clase base (reutilizamos su código)
        super().__init__(codigo, nombre, precio, stock)
        # Atributos específicos del panel solar
        self.potencia_watts = potencia_watts
        self.eficiencia = eficiencia  # en porcentaje

    # --- Polimorfismo ---
    # Mismo nombre de método que en la clase base, pero con otro comportamiento.
    def ficha_tecnica(self):
        ficha_base = super().ficha_tecnica()  # reutilizamos la ficha de la base
        return (
            f"{ficha_base}\n"
            f"  Tipo: Panel Solar\n"
            f"  Potencia: {self.potencia_watts} W\n"
            f"  Eficiencia: {self.eficiencia}%"
        )

    def to_dict(self):
        datos = super().to_dict()          # diccionario de la clase base
        datos["tipo"] = "PanelSolar"       # corregimos el tipo
        datos["potencia_watts"] = self.potencia_watts
        datos["eficiencia"] = self.eficiencia
        return datos


# -------------------------------------------------------------
# Punto B: Persistencia y gestión del catálogo
# -------------------------------------------------------------

class GestorInventario:
    """Se encarga de guardar el catálogo en disco."""

    def guardar_catalogo_json(self, lista_dispositivos, ruta_archivo):
        """Convierte cada dispositivo en diccionario y guarda la lista en un archivo JSON."""
        catalogo = []
        for dispositivo in lista_dispositivos:
            catalogo.append(dispositivo.to_dict())

        try:
            # "w" = modo escritura; encoding utf-8 para respetar tildes
            with open(ruta_archivo, "w", encoding="utf-8") as archivo:
                json.dump(catalogo, archivo, indent=4, ensure_ascii=False)
        except OSError as error:
            print(f"No se pudo guardar el catálogo: {error}")
            return False
        else:
            print(f"Catálogo guardado con éxito: {len(catalogo)} productos en '{ruta_archivo}'.")
            return True


# -------------------------------------------------------------
# Bloque de prueba
# -------------------------------------------------------------
if __name__ == "__main__":

    # 1) Creamos productos válidos
    lampara = DispositivoEcológico("ECO-100", "Lámpara LED Solar", 15000.0, 40)
    panel_1 = PanelSolar("PS-200", "Panel Solar Monocristalino", 185000.0, 12, 450, 21.5)
    panel_2 = PanelSolar("PS-300", "Panel Solar Policristalino", 140000.0, 8, 330, 17.0)

    catalogo_valido = [lampara, panel_1, panel_2]

    # 2) Polimorfismo: el mismo llamado .ficha_tecnica() da resultados distintos
    print("=== FICHAS TÉCNICAS ===")
    for producto in catalogo_valido:
        print(producto.ficha_tecnica())
        print("-" * 40)

    # 3) Prueba de captura controlada: intentamos poner stock negativo
    print("\n=== PRUEBA DE VALIDACIÓN DE STOCK ===")
    try:
        panel_1.stock = -5
    except StockInvalidoError as error:
        print(f"Error capturado correctamente: {error}")
    print(f"El stock de '{panel_1.nombre}' sigue en {panel_1.stock} unidades.")

    # 4) Otro intento erróneo: crear un producto con stock negativo
    try:
        panel_roto = PanelSolar("PS-999", "Panel Defectuoso", 99000.0, -3, 300, 15.0)
        catalogo_valido.append(panel_roto)  # esta línea NO llega a ejecutarse
    except StockInvalidoError as error:
        print(f"Error capturado correctamente: {error}")
        print("El producto no se agregó al catálogo.")

    # 5) Exportamos solo los productos válidos al archivo JSON
    print("\n=== EXPORTACIÓN DEL CATÁLOGO ===")
    # Guardamos el JSON en la misma carpeta que este archivo .py
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_json = os.path.join(carpeta_actual, "catalogo_ecotech.json")

    gestor = GestorInventario()
    gestor.guardar_catalogo_json(catalogo_valido, ruta_json)