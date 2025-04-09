# Reto Algoritmos y Estructuras de Datos

Este proyecto implementa soluciones a problemas clásicos de algoritmos y estructuras de datos, como el **Recorrido del Caballo**, **Torre de Hanoi**, y **N Reinas**, utilizando Python y una interfaz gráfica interactiva con **Gradio**.

## Tabla de Contenidos

- [Descripción](#descripción)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

## Descripción

El proyecto incluye las siguientes funcionalidades:

1. **Recorrido del Caballo**: Encuentra un recorrido válido para un caballo de ajedrez en un tablero de tamaño NxN.
2. **Torre de Hanoi**: Resuelve el problema de mover discos entre varillas siguiendo las reglas de la Torre de Hanoi.
3. **N Reinas**: Encuentra todas las soluciones posibles para colocar N reinas en un tablero NxN sin que se ataquen entre sí.

Los resultados se almacenan en una base de datos SQLite para su posterior consulta.

## Requisitos

- Python 3.10 o superior
- Librerías especificadas en `requirements.txt`

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/alex6036/Reto_Algoritmos_y_Estructuras_de_Datos.git
   cd Reto_Algoritmos_y_Estructuras_de_Datos

   .
├── [main.py](http://_vscodecontentref_/1)                 # Archivo principal que lanza la aplicación
├── [problemas_clasicos.db](http://_vscodecontentref_/2)   # Base de datos SQLite para almacenar resultados
├── caballo/                # Módulo para el problema del Recorrido del Caballo
│   ├── [caballos.py](http://_vscodecontentref_/3)
│   └── [__init__.py](http://_vscodecontentref_/4)
├── hanoi/                  # Módulo para el problema de la Torre de Hanoi
│   ├── [hanoi.py](http://_vscodecontentref_/5)
│   └── [__init__.py](http://_vscodecontentref_/6)
├── reina/                  # Módulo para el problema de las N Reinas
│   ├── [reina.py](http://_vscodecontentref_/7)
│   └── [__init__.py](http://_vscodecontentref_/8)
├── nodo/                   # Módulo vacío (posible uso futuro)
├── [requirements.txt](http://_vscodecontentref_/9)        # Dependencias del proyecto
└── [README.md](http://_vscodecontentref_/10)               # Documentación del proyecto