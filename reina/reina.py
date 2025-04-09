# reina/reina.py
from sqlalchemy.orm import Session
from main import engine, SolucionReinas

class NReinas:
    def __init__(self, n):
        self.n = n  # Número de reinas (y tamaño del tablero NxN)
        self.soluciones = []  # Lista para almacenar las soluciones

    def es_seguro(self, tablero, fila, columna):
        # Verifica si es seguro colocar una reina en (fila, columna)
        for i in range(fila):
            if tablero[i] == columna or \
               tablero[i] - i == columna - fila or \
               tablero[i] + i == columna + fila:
                return False
        return True

    def resolver_reinas(self, fila=0, tablero=None):
        # Inicializar tablero como una lista vacía si no se proporciona
        if tablero is None:
            tablero = []

        # Caso base: si hemos colocado todas las reinas, guardar la solución
        if fila == self.n:
            self.soluciones.append(tablero[:])
            return

        # Probar cada columna en la fila actual
        for columna in range(self.n):
            if self.es_seguro(tablero, fila, columna):
                tablero.append(columna)
                self.resolver_reinas(fila + 1, tablero)
                tablero.pop()

    def mostrar_soluciones(self):
        # Mostrar las soluciones en un formato legible
        if not self.soluciones:
            return "No se encontraron soluciones para este número de reinas."
        resultado = []
        for idx, solucion in enumerate(self.soluciones, 1):
            tablero = []
            for fila in range(len(solucion)):
                fila_str = ['Q' if columna == solucion[fila] else '.' for columna in range(len(solucion))]
                tablero.append(' '.join(fila_str))
            resultado.append(f"Solución {idx}:\n" + "\n".join(tablero) + "\n")
        return "\n".join(resultado)

    def resolver(self):
        # Método para resolver el problema (para compatibilidad con main.py)
        self.soluciones = []
        self.resolver_reinas()
        return self.mostrar_soluciones()

    def guardar_en_base_de_datos(self):
        session = Session(bind=engine)
        for solucion_id, solucion in enumerate(self.soluciones, 1):
            for columna, fila in enumerate(solucion):
                posicion = SolucionReinas(solucion_id=solucion_id, columna=columna, fila=fila)
                session.add(posicion)
        session.commit()
        session.close()