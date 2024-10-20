import os
import osmnx as ox

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Instancia de Puerto Montt
    # CODIGO QUE LA AYUDANTE PUSO EN EL PPT
north = -41.4
south = -41.496
east = -72.85
west = -73.03
G0 = ox.graph_from_bbox(north,south,east,west,network_type='drive')

    # Elimino los arcos paralelos, esto con el código que puso la ayudante
G = G0.copy()
duplicated = []
for u,v,a in G.edges(data=True):
    if len(G[u][v]) == 2:
        duplicated.append((u,v,1))
    elif len(G[u][v]) == 3:      
        duplicated.append((u,v,1))
        duplicated.append((u,v,2))
duplicated = list(dict.fromkeys(duplicated))

G.remove_edges_from(duplicated)

# ESTO GRAFICA EL MAPA DE PTO MONTT Y PONE LOS NODOS DE PRODUCCION, BODEGA Y DEMANDA
'''colores = {'demanda':'blue','bodega':'green','produccion':'black'}
m=ox.folium.plot_graph_folium(G0, tiles='CartoDB positron', color='red', weight=1)
for i in range(len(nodos_totales)):
    nodo = nodos_totales.loc[i]
    x = nodo['x']
    y = nodo['y']
    tipo = nodo['tipo']
    folium.CircleMarker(location=[y, x], color = colores[tipo], radius=5, fill = True, fill_opacity = 10).add_to(m)
m'''

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