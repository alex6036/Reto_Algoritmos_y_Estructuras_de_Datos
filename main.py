# main.py
import gradio as gr
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Crear conexión y base de datos
engine = create_engine("sqlite:///problemas_clasicos.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# --- Definir las tablas ---
class MovimientoCaballo(Base):
    __tablename__ = 'movimientos_caballo'
    id = Column(Integer, primary_key=True)
    paso = Column(Integer)
    fila = Column(Integer)
    columna = Column(Integer)

    def __repr__(self):
        return f"Paso {self.paso}: ({self.fila}, {self.columna})"

class MovimientoHanoi(Base):
    __tablename__ = 'movimientos_hanoi'
    id = Column(Integer, primary_key=True)
    paso = Column(Integer)
    origen = Column(String)
    destino = Column(String)

    def __repr__(self):
        return f"Paso {self.paso}: Mover disco desde {self.origen} a {self.destino}"

class SolucionReinas(Base):
    __tablename__ = 'soluciones_reinas'
    id = Column(Integer, primary_key=True)
    solucion_id = Column(Integer)  # Identificador de la solución (en caso de múltiples soluciones)
    columna = Column(Integer)
    fila = Column(Integer)

    def __repr__(self):
        return f"Solución {self.solucion_id} - Columna {self.columna}: Fila {self.fila}"

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Importar los módulos
try:
    from caballo.caballos import CaballoAjedrez
    print("CaballoAjedrez importado correctamente")
except Exception as e:
    print(f"Error al importar CaballoAjedrez: {e}")

try:
    from hanoi.hanoi import TorreDeHanoi
    print("TorreDeHanoi importado correctamente")
except Exception as e:
    print(f"Error al importar TorreDeHanoi: {e}")

try:
    from reina.reina import NReinas
    print("NReinas importado correctamente")
except Exception as e:
    print(f"Error al importar NReinas: {e}")

# --- Funciones para el Recorrido del Caballo ---
def resolver_caballo(tamano, fila_inicial, columna_inicial):
    try:
        tamano = int(tamano)
        fila_inicial = int(fila_inicial)
        columna_inicial = int(columna_inicial)

        if tamano < 1 or fila_inicial < 0 or columna_inicial < 0 or fila_inicial >= tamano or columna_inicial >= tamano:
            return "Error: Los valores deben estar dentro del rango del tablero."

        caballo = CaballoAjedrez(tamano)
        if caballo.resolver(fila_inicial, columna_inicial):
            tablero = "\n".join([" ".join(f"{celda:2}" for celda in fila) for fila in caballo.tablero])
            recorrido = "\n".join([f"Paso {i}: {pos}" for i, pos in enumerate(caballo.recorrido)])
            caballo.guardar_en_base_de_datos()
            return f"Tablero:\n{tablero}\n\nRecorrido:\n{recorrido}"
        else:
            return "No se encontró una solución para el recorrido del caballo."
    except ValueError:
        return "Error: Ingresa solo números válidos."
    except Exception as e:
        return f"Error en resolver_caballo: {e}"

# --- Funciones para la Torre de Hanoi ---
def resolver_hanoi_wrapper(discos, origen, destino, auxiliar):
    try:
        discos = int(discos)
        if discos < 1:
            return "Error: El número de discos debe ser mayor que 0."
        hanoi_app = TorreDeHanoi()
        resultado = hanoi_app.resolver_torre_hanoi(discos, origen, destino, auxiliar)
        hanoi_app.guardar_en_base_de_datos()
        return resultado if resultado else "No se encontraron movimientos."
    except ValueError:
        return "Error: Ingresa un número válido de discos."
    except Exception as e:
        return f"Error en resolver_hanoi_wrapper: {e}"

# --- Funciones para las N Reinas ---
def resolver_reinas_wrapper(numero_reinas):
    try:
        n = int(numero_reinas)
        if n < 1:
            return "Error: El número de reinas debe ser mayor que 0."
        reinas_app = NReinas(n)
        resultado = reinas_app.resolver()
        reinas_app.guardar_en_base_de_datos()
        return resultado if resultado else "No se encontraron soluciones."
    except ValueError:
        return "Error: Ingresa un número válido de reinas."
    except Exception as e:
        return f"Error en resolver_reinas_wrapper: {e}"

# --- Interfaz Gradio ---
with gr.Blocks(title="Problemas Clásicos") as app:
    gr.Markdown("# Problemas Clásicos de Algoritmos")
    
    tabs = gr.Tabs()
    with tabs:
        # Tab de Caballo
        with gr.Tab("Recorrido del Caballo"):
            print("Renderizando tab Recorrido del Caballo")
            gr.Markdown("""
            Ingresa el tamaño del tablero y la posición inicial del caballo para resolver el problema del recorrido.
            """)
            tamano = gr.Textbox(label="Tamaño del tablero (N x N)", value="8")
            fila = gr.Textbox(label="Fila inicial (0 a N-1)", value="0")
            columna = gr.Textbox(label="Columna inicial (0 a N-1)", value="0")
            output_caballo = gr.Textbox(label="Resultado", lines=10)
            gr.Button("Resolver").click(
                fn=resolver_caballo, 
                inputs=[tamano, fila, columna], 
                outputs=output_caballo
            )

        # Tab de Torre de Hanoi
        with gr.Tab("Torre de Hanoi"):
            print("Renderizando tab Torre de Hanoi")
            gr.Markdown("""
            Ingresa el número de discos y las varillas para resolver la Torre de Hanoi.
            """)
            discos = gr.Textbox(label="Número de discos", value="3")
            origen = gr.Textbox(label="Varilla de origen", value="A")
            destino = gr.Textbox(label="Varilla de destino", value="C")
            auxiliar = gr.Textbox(label="Varilla auxiliar", value="B")
            output_hanoi = gr.Textbox(label="Movimientos", lines=10)
            gr.Button("Resolver").click(
                fn=resolver_hanoi_wrapper, 
                inputs=[discos, origen, destino, auxiliar], 
                outputs=output_hanoi
            )

        # Tab de N Reinas
        with gr.Tab("N Reinas"):
            print("Renderizando tab N Reinas")
            gr.Markdown("""
            Ingresa el número de reinas para resolver el problema de las N Reinas.
            """)
            n_reinas = gr.Textbox(label="Número de reinas", value="4")
            output_reinas = gr.Textbox(label="Soluciones", lines=10)
            gr.Button("Resolver").click(
                fn=resolver_reinas_wrapper, 
                inputs=[n_reinas], 
                outputs=output_reinas
            )

# Lanzar la aplicación
if __name__ == "__main__":
    app.launch()