from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

# Crear conexión y base de datos
engine = create_engine("sqlite:///recorrido_caballo.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# --- Definir la tabla ---
class MovimientoCaballo(Base):
    __tablename__ = 'movimientos'
    id = Column(Integer, primary_key=True)
    paso = Column(Integer)
    fila = Column(Integer)
    columna = Column(Integer)

    def __repr__(self):
        return f"Paso {self.paso}: ({self.fila}, {self.columna})"

# Crear la tabla en la base de datos
Base.metadata.create_all(engine)

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
        print(f"Comenzando desde la posición: ({x}, {y})")
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

    def imprimir_tablero(self):
        for fila in self.tablero:
            print(" ".join(f"{celda:2}" for celda in fila))

    def imprimir_recorrido_columna(self):
        print("Recorrido en columna:")
        for pos in self.recorrido:
            print(pos)

    def guardar_en_base_de_datos(self):
        session = Session()
        for paso, (fila, columna) in enumerate(self.recorrido):
            movimiento = MovimientoCaballo(paso=paso, fila=fila, columna=columna)
            session.add(movimiento)
        session.commit()
        session.close()
        print("Recorrido guardado en la base de datos.")
        
