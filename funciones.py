import pandas as pd
import networkx as nx
import numpy as np
import os
import osmnx as ox

# ESTO ENCUENTRAS LAS RUTAS MINIMAS ENTRE CUALQUIER PAR DE NODOS, DA IGUAL SI ES PRODUCCION, ALMACENAJE O DEMANDA
# N son las rutas minimas de los N-primeros arcos del grafo G (de los 1,2...,n arcos)

def rutas_min(grafo: nx.Graph, grafo_ciudad: nx.Graph, N: int):
    lista_pares_nodos = list(grafo.edges())
    dict_info_nodos = dict(grafo_ciudad.nodes(data=True))

    rutas = []
    distancias = []

    for par in range(N):
        parcito = lista_pares_nodos[par]
        O = parcito[0]
        D = parcito[1]

        x_O = dict_info_nodos[O]['x']
        y_O = dict_info_nodos[O]['y']
        
        x_D = dict_info_nodos[D]['x']
        y_D = dict_info_nodos[D]['y']
        
        origen = ox.distance.nearest_nodes(grafo_ciudad, x_O, y_O)
        destino = ox.distance.nearest_nodes(grafo_ciudad, x_D, y_D)

        r = nx.shortest_path(grafo_ciudad, origen, destino, weight='length')
        d = nx.shortest_path_length(grafo_ciudad, origen, destino, weight='distance')
        rutas.append(r)
        distancias.append(d)
    
    # rutas son las rutas minimas del arco i del grafo vial, distancias es el largo de la ruta io
    return (rutas,distancias)

# la funcion que grafica rutas minimas
def graficar_rutas_min_n(rutas: list, grafo):
    m2 = ox.folium.plot_graph_folium(grafo.subgraph(rutas[0]), tiles='CartoDB positron', weight= 2)
    for a in range(1, len(rutas)):
        ox.folium.plot_graph_folium(grafo.subgraph(rutas[a]) , graph_map = m2, tiles='CartoDB positron', weight= 2)

    # Guardar mapa como html
    map_file2 = 'Mapa de prueba.html'
    m2.save(map_file2)
    print(f"Mapa guardado en {map_file2}")
    
    return m2

class Node:
    def __init__(self, id, x, y, tipo, numero):
        self.x = x
        self.y = y
        self.id = id
        self.tipo = tipo
        self.numero = numero