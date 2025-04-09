# caballo/caballos.py
from sqlalchemy.orm import Session
from main import engine, MovimientoCaballo

# --- Clase CaballoAjedrez ---
class CaballoAjedrez:
    def __init__(self, tamaño=8):
        self.N = tamaño
        self.tablero = [[-1 for _ in range(self.N)] for _ in range(self.N)]
        self.movimientos = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]
        self.recorrido = []

    def es_valido(self, x, y):
        return 0 <= x < self.N and 0 <= y < self.N and self.tablero[x][y] == -1

    def resolver(self, x=0, y=0):
        self.tablero[x][y] = 0
        self.recorrido.append((x, y))
        if self._recorrer(x, y, 1):
            return True
        else:
            self.tablero[x][y] = -1
            self.recorrido.pop()
            return False

    def _recorrer(self, x, y, paso):
        if paso == self.N * self.N:
            return True

        for dx, dy in self.movimientos:
            nx, ny = x + dx, y + dy
            if self.es_valido(nx, ny):
                self.tablero[nx][ny] = paso
                self.recorrido.append((nx, ny))
                if self._recorrer(nx, ny, paso + 1):
                    return True
                self.tablero[nx][ny] = -1
                self.recorrido.pop()
        return False

    def guardar_en_base_de_datos(self):
        session = Session(bind=engine)
        for paso, (fila, columna) in enumerate(self.recorrido):
            movimiento = MovimientoCaballo(paso=paso, fila=fila, columna=columna)
            session.add(movimiento)
        session.commit()
        session.close()