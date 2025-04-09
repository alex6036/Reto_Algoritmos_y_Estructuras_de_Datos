# hanoi/hanoi.py
import gradio as gr

class TorreDeHanoi:
    def __init__(self):
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
            n = int(n)
            if n < 1:
                return "Error: El número de discos debe ser al menos 1."
            movimientos = self.hanoi(n, 'A', 'C', 'B')
            return self.imprimir_movimientos(movimientos)
        except ValueError:
            return "Error: Por favor, ingrese un número válido."