from caballo.caballos import CaballoAjedrez
import gradio as gr

# --- Función para Gradio ---
def resolver_caballo(inicio, final):
    try:
        inicio = int(inicio)
        final = int(final)
        
        # Validar que los valores estén en el rango permitido (0 a 7)
        if not (0 <= inicio <= 7 and 0 <= final <= 7):
            return "Error: Los valores deben estar entre 0 y 7."
        
        caballo = CaballoAjedrez()
        if caballo.resolver(inicio, final):
            # Capturar la salida del tablero y recorrido como texto
            tablero = "\n".join([" ".join(f"{celda:2}" for celda in fila) for fila in caballo.tablero])
            recorrido = "\n".join([f"Paso {i}: {pos}" for i, pos in enumerate(caballo.recorrido)])
            caballo.guardar_en_base_de_datos()
            return f"Tablero:\n{tablero}\n\nRecorrido:\n{recorrido}"
        else:
            return "No se encontró solución."
    except ValueError:
        return "Error: Por favor, ingrese valores numéricos válidos."

# --- Interfaz de Gradio ---
interfaz = gr.Interface(
    fn=resolver_caballo,
    inputs=[
        gr.Textbox(label="Fila inicial (0 a 7)", value="0"),
        gr.Textbox(label="Columna inicial (0 a 7)", value="0")
    ],
    outputs="text",
    title="Recorrido del Caballo",
    description="Ingresa la fila y columna iniciales (entre 0 y 7) para resolver el recorrido del caballo en un tablero 8x8."
)

# Lanzar la interfaz
if __name__ == "__main__":
    interfaz.launch()