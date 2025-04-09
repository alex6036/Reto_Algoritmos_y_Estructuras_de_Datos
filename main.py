from caballo.caballos import CaballoAjedrez
from hanoi.hanoi import TorreDeHanoi

import gradio as gr
import traceback

# --- Clase TorreDeHanoi (definida aquí para evitar problemas de importación) ---
class TorreDeHanoi:
    def __init__(self):
        print("Inicializando TorreDeHanoi...")
        pass

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

    def resolver_torre_hanoi(self, n):
        try:
            print(f"Resolviendo Torre de Hanoi para {n} discos...")
            n = int(n)
            if n < 1:
                return "Error: El número de discos debe ser al menos 1."
            movimientos = self.hanoi(n, 'A', 'C', 'B')
            return self.imprimir_movimientos(movimientos)
        except ValueError:
            return "Error: Por favor, ingrese un número válido."

# --- Funciones para el Recorrido del Caballo ---
def resolver_caballo(tamaño, inicio, final):
    try:
        print(f"Resolviendo Recorrido del Caballo con tamaño={tamaño}, inicio={inicio}, final={final}...")
        tamaño = int(tamaño)
        inicio = int(inicio)
        final = int(final)

        if tamaño < 1 or inicio < 0 or final < 0 or inicio >= tamaño or final >= tamaño:
            return "Error: Los valores deben ser válidos y dentro del tamaño del tablero."

        caballo = CaballoAjedrez(tamaño)
        if caballo.resolver(inicio, final):
            tablero = "\n".join([" ".join(f"{celda:2}" for celda in fila) for fila in caballo.tablero])
            recorrido = "\n".join([f"Paso {i}: {pos}" for i, pos in enumerate(caballo.recorrido)])
            caballo.guardar_en_base_de_datos()
            return f"Tablero:\n{tablero}\n\nRecorrido:\n{recorrido}"
        else:
            return "No se encontró una solución para el recorrido del caballo con los parámetros dados."
    except ValueError:
        return "Error: Por favor, ingrese valores numéricos válidos."

# --- Crear las interfaces ---
try:
    # Interfaz para el Caballo
    caballo_interfaz = gr.Interface(
        fn=resolver_caballo,
        inputs=[
            gr.Textbox(label="Tamaño del tablero (N x N)", value="8"),
            gr.Textbox(label="Fila inicial (0 a N-1)", value="0"),
            gr.Textbox(label="Columna inicial (0 a N-1)", value="0")
        ],
        outputs=gr.Textbox(label="Resultado"),
        title="Recorrido del Caballo",
        description="Ingresa el tamaño del tablero y la posición inicial del caballo para resolver el problema del recorrido. El resultado mostrará el tablero y el recorrido paso a paso."
    )
    print("Interfaz del Caballo creada con éxito.")

    # Instanciar TorreDeHanoi y crear su interfaz
    try:
        hanoi_app = TorreDeHanoi()
        print("Instancia de TorreDeHanoi creada con éxito.")
        hanoi_interfaz = gr.Interface(
            fn=hanoi_app.resolver_torre_hanoi,
            inputs=gr.Slider(
                minimum=1,
                maximum=6,
                step=1,
                value=3,
                label="Número de discos"
            ),
            outputs=gr.Textbox(label="Movimientos"),
            title="Torre de Hanoi",
            description="Selecciona el número de discos y observa los pasos para resolver la Torre de Hanoi.",
            live=True
        )
        print("Interfaz de Hanoi creada con éxito.")
    except Exception as e:
        print(f"Error al crear la interfaz de Hanoi: {e}")
        traceback.print_exc()
        hanoi_interfaz = gr.Interface(
            fn=lambda x: "Error: No se pudo cargar la interfaz de la Torre de Hanoi.",
            inputs=gr.Slider(minimum=1, maximum=6, step=1, value=3, label="Número de discos"),
            outputs=gr.Textbox(label="Movimientos"),
            title="Torre de Hanoi",
            description="Error al cargar la Torre de Hanoi."
        )

except Exception as e:
    print(f"Error al crear las interfaces: {e}")
    traceback.print_exc()

# --- Menú con pestañas ---
try:
    menu = gr.TabbedInterface(
        [caballo_interfaz, hanoi_interfaz],
        tab_names=["Recorrido del Caballo", "Torre de Hanoi"],
        title="Menú de Problemas Clásicos"
    )
    print("Menú creado con éxito.")
except Exception as e:
    print(f"Error al crear el menú: {e}")
    traceback.print_exc()

# Lanzar el menú
if __name__ == "__main__":
    try:
        menu.launch()
    except Exception as e:
        print(f"Error al lanzar el menú: {e}")
        traceback.print_exc()