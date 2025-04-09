# hanoi/hanoi.py
from sqlalchemy.orm import Session
from main import engine, MovimientoHanoi

class TorreDeHanoi:
    def __init__(self):
        self.movimientos = []

    def hanoi(self, n, origen, destino, auxiliar, movimientos=None):
        if movimientos is None:
            movimientos = []
        if n == 1:
            movimientos.append((origen, destino))
        else:
            self.hanoi(n-1, origen, auxiliar, destino, movimientos)
            movimientos.append((origen, destino))
            self.hanoi(n-1, auxiliar, destino, origen, movimientos)
        return movimientos

    def imprimir_movimientos(self, movimientos):
        return "\n".join([f"Paso {i+1}: Mover disco desde {mov[0]} a {mov[1]}" for i, mov in enumerate(movimientos)])

    def resolver_torre_hanoi(self, n, origen, destino, auxiliar):
        try:
            n = int(n)
            if n < 1:
                return "Error: El número de discos debe ser al menos 1."
            self.movimientos = self.hanoi(n, origen, destino, auxiliar)
            return self.imprimir_movimientos(self.movimientos)
        except ValueError:
            return "Error: Por favor, ingrese un número válido."

    def guardar_en_base_de_datos(self):
        session = Session(bind=engine)
        for paso, (origen, destino) in enumerate(self.movimientos):
            movimiento = MovimientoHanoi(paso=paso, origen=origen, destino=destino)
            session.add(movimiento)
        session.commit()
        session.close()