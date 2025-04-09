from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
import gradio as gr

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

    def obtener_tablero(self):
        return "\n".join([" ".join(f"{celda:2}" for celda in fila) for fila in self.tablero])

    def obtener_recorrido(self):
        return "\n".join([f"Paso {i}: {pos}" for i, pos in enumerate(self.recorrido)])

    def guardar_en_base_de_datos(self):
        session = Session()
        for paso, (fila, columna) in enumerate(self.recorrido):
            movimiento = MovimientoCaballo(paso=paso, fila=fila, columna=columna)
            session.add(movimiento)
        session.commit()
        session.close()

# --- Función para Gradio ---
def resolver_recorrido(tamaño, fila_inicial, columna_inicial):
    try:
        tamaño = int(tamaño)
        fila_inicial = int(fila_inicial)
        columna_inicial = int(columna_inicial)

        if tamaño < 1 or fila_inicial < 0 or columna_inicial < 0 or fila_inicial >= tamaño or columna_inicial >= tamaño:
            return "Error: Los valores deben ser válidos y dentro del tamaño del tablero."

        caballo = CaballoAjedrez(tamaño)
        if caballo.resolver(fila_inicial, columna_inicial):
            caballo.guardar_en_base_de_datos()
            return f"Tablero:\n{caballo.obtener_tablero()}\n\nRecorrido:\n{caballo.obtener_recorrido()}"
        else:
            return "No se encontró una solución para el recorrido del caballo con los parámetros dados."
    except ValueError:
        return "Error: Por favor, ingrese valores numéricos válidos."

# --- Interfaz de Gradio ---
interfaz = gr.Interface(
    fn=resolver_recorrido,
    inputs=[
        gr.Textbox(label="Tamaño del tablero (N x N)", value="8"),
        gr.Textbox(label="Fila inicial (0 a N-1)", value="0"),
        gr.Textbox(label="Columna inicial (0 a N-1)", value="0")
    ],
    outputs="text",
    title="Recorrido del Caballo",
    description="Ingresa el tamaño del tablero y la posición inicial del caballo para resolver el problema del recorrido. El resultado mostrará el tablero y el recorrido paso a paso."
)

# Lanzar la interfaz
interfaz.launch()