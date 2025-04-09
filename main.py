from caballo.caballos import CaballoAjedrez

# --- Ejemplo de uso ---
if __name__ == "__main__":
    caballo = CaballoAjedrez()
    inicio = int(input('Escribe un numero del 0 al 7\n'))
    final = int(input('Escribe otro numero del 0 al 7\n'))
    if caballo.resolver(inicio, final):  # Puedes cambiar las coordenadas aquí
        caballo.imprimir_tablero()
        print()
        caballo.imprimir_recorrido_columna()
        caballo.guardar_en_base_de_datos()  # Guarda en la base de datos
    else:
        print("No se encontró solución.")