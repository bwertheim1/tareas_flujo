import os
import osmnx as ox

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# PROCESAMIENTO DE TODAS LAS TABLAS
    # RUTAS RELATIVAS
RUTA1 = os.path.join('datos','ubicacion_produccion.csv')
RUTA2 = os.path.join('datos',"ubicacion_bodegas_adicionales.csv")
RUTA3 = os.path.join('datos',"ubicacion_demanda.csv")
RUTA4 = os.path.join('datos','precio_venta.csv')
RUTA5 = os.path.join('datos',"oferta_min_proveedores.csv")
RUTA6 = os.path.join('datos',"oferta_max_proveedores.csv")
RUTA7 = os.path.join('datos',"inventario_inicial.csv")
RUTA8 = os.path.join('datos',"inventario_inicial_adicional.csv")
RUTA9 = os.path.join('datos',"demanda_min.csv")
RUTA10 = os.path.join('datos',"demanda_max.csv")
RUTA11 = os.path.join('datos',"costo_produccion.csv")
RUTA12 = os.path.join('datos',"costo_fijo_bodega_adicional.csv")
RUTA13 = os.path.join('datos',"costo_almacenaje_adicional.csv")
RUTA14 = os.path.join('datos',"costo_almacenaje.csv")
RUTA15 = os.path.join('datos',"capacidad_almacenaje.csv")
RUTA16 = os.path.join('datos',"capacidad_almacenaje_adicional.csv")

T = 8
P = 7
B = 18
D = 24

c_tte = 12