# -*- coding: utf-8 -*-
"""T2 flujo.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RRZj6SE4_TSE-DMUbdFkEq-ko9NXAOrK
"""
import funciones as ff
import pandas as pd
import networkx as nx
import numpy as np
import osmnx as ox
import parametros as R

lista = []
for i in range(1,R.T+1):
    lista.append(str(i))

id_prod = []
for a in range(1,R.P+1):
    id_prod.append(f'P{a}')

id_bod = []
for a in range(1,R.B+1):
    id_bod.append(f'B{a}')

id_dem = []
for a in range(1,R.D+1):
    id_dem.append(f'D{a}')

# LECTURA DATOS Y CREACIÓN DE TABLAS
    # PRODUCCION
ubicacion_produccion = pd.read_csv(R.RUTA1)
oferta_min_proveedores = pd.read_csv(R.RUTA5)
oferta_max_proveedores = pd.read_csv(R.RUTA6)
inventario_inicial = pd.read_csv(R.RUTA7)
costo_produccion = pd.read_csv(R.RUTA11)
costo_almacenaje = pd.read_csv(R.RUTA14)
capacidad_almacenaje = pd.read_csv(R.RUTA15)

    # BODEGAS
ubicacion_bodegas = pd.read_csv(R.RUTA2)
inventario_inicial_adicional = pd.read_csv(R.RUTA8)
costo_fijo_bodega_adicional = pd.read_csv(R.RUTA12)
costo_almacenaje_adicional = pd.read_csv(R.RUTA13)
capacidad_almacenaje_adicional = pd.read_csv(R.RUTA16)

    # DEMANDA
ubicacion_demanda = pd.read_csv(R.RUTA3)
demanda_min = pd.read_csv(R.RUTA9)
demanda_max = pd.read_csv(R.RUTA10)
precio_venta = pd.read_csv(R.RUTA4)


# Se crea un DataFrame combinado con todos los nodos y ubicaciones
nodos_produccion = ubicacion_produccion[['id_nodo', 'x', 'y']].copy()
nodos_produccion['tipo'] = 'produccion'
nodos_produccion = nodos_produccion[0:R.P]
nodos_produccion['id'] = id_prod


nodos_bodegas = ubicacion_bodegas[['id_nodo', 'x', 'y']].copy()
nodos_bodegas['tipo'] = 'bodega'
nodos_bodegas = nodos_bodegas[0:R.B]
nodos_bodegas['id'] = id_bod


nodos_demanda = ubicacion_demanda[['id_nodo', 'x', 'y']].copy()
nodos_demanda['tipo'] = 'demanda'
nodos_demanda = nodos_demanda[0:R.D]
nodos_demanda['id'] = id_dem


    # CREO TABLAS CON LA INFO DE LOS NODOS EN CADA PERDIODO
        # DEMANDA
precio_venta = precio_venta[lista]
precio_venta['tipo'] = 'demanda'
precio_venta = precio_venta[0:R.D]
precio_venta['id'] = id_dem


demanda_min = demanda_min[lista]
demanda_min['tipo'] = 'demanda'
demanda_min = demanda_min[0:R.D]
demanda_min['id'] = id_dem

demanda_max = demanda_max[lista]
demanda_max['tipo'] = 'demanda'
demanda_max = demanda_max[0:R.D]
demanda_max['id'] = id_dem

        # PRODUCCION
oferta_min_proveedores =oferta_min_proveedores[lista]
oferta_min_proveedores['tipo'] = 'produccion'
oferta_min_proveedores = oferta_min_proveedores[0:R.P]
oferta_min_proveedores['id'] = id_prod

oferta_max_proveedores = oferta_max_proveedores[lista]
oferta_max_proveedores['tipo'] = 'produccion'
oferta_max_proveedores = oferta_max_proveedores[0:R.P]
oferta_max_proveedores['id'] = id_prod

inventario_inicial = inventario_inicial[['1']]
inventario_inicial['tipo'] = 'produccion'
inventario_inicial = inventario_inicial[0:R.P]
inventario_inicial['id'] = id_prod

costo_produccion = costo_produccion[lista]
costo_produccion['tipo'] = 'produccion'
costo_produccion = costo_produccion[0:R.P]
costo_produccion['id'] = id_prod

costo_almacenaje = costo_almacenaje[lista]
costo_almacenaje['tipo'] = 'produccion'
costo_almacenaje = costo_almacenaje[0:R.P]
costo_almacenaje['id'] = id_prod

capacidad_almacenaje = capacidad_almacenaje[lista]
capacidad_almacenaje['tipo'] = 'produccion'
capacidad_almacenaje = capacidad_almacenaje[0:R.P]
capacidad_almacenaje['id'] = id_prod

        # BODEGAS
inventario_inicial_adicional = inventario_inicial_adicional[['1']]
inventario_inicial_adicional['tipo'] = 'bodega'
inventario_inicial_adicional = inventario_inicial_adicional[0:R.B]
inventario_inicial_adicional['id'] = id_bod

costo_fijo_bodega_adicional = costo_fijo_bodega_adicional[['1']]
costo_fijo_bodega_adicional['tipo'] = 'bodega'
costo_fijo_bodega_adicional = costo_fijo_bodega_adicional[0:R.B]
costo_fijo_bodega_adicional['id'] = id_bod

costo_almacenaje_adicional = costo_almacenaje_adicional[lista]
costo_almacenaje_adicional['tipo'] = 'bodega'
costo_almacenaje_adicional = costo_almacenaje_adicional[0:R.B]
costo_almacenaje_adicional['id'] = id_bod

capacidad_almacenaje_adicional = capacidad_almacenaje_adicional[lista]
capacidad_almacenaje_adicional['tipo'] = 'bodega'
capacidad_almacenaje_adicional = capacidad_almacenaje_adicional[0:R.B]
capacidad_almacenaje_adicional['id'] = id_bod

# Se combina en un solo DataFrame
nodos_totales = pd.concat([nodos_produccion, nodos_bodegas, nodos_demanda], ignore_index=True)

# Se crea un grafo para representar la red
grafo_vial = nx.Graph()

# Se añaden los nodos al grafo
for _, row in nodos_totales.iterrows():
    grafo_vial.add_node(row['id'], id_nodo=row['id_nodo'], pos=(row['x'], row['y']), tipo=row['tipo'])



# Se añaden los vertices con distancia entre todos los nodos
for i, nodo_i in nodos_totales.iterrows():
    for j, nodo_j in nodos_totales.iterrows():
        if i < j:  # Evitar duplicados
            distancia = np.sqrt((nodo_i['x'] - nodo_j['x'])**2 + (nodo_i['y'] - nodo_j['y'])**2)
            grafo_vial.add_edge(nodo_i['id_nodo'], nodo_j['id_nodo'], weight=distancia)             # creo que esto debería ser con los nodos dentro del mapa - Vale

# Se crea matriz de costos por transporte
nodos_relevantes = list(grafo_vial.nodes)
num_nodos = len(nodos_relevantes)
matriz_distancias = np.zeros((num_nodos, num_nodos))

# RESETEO LOS INDICES
capacidad_almacenaje_adicional = capacidad_almacenaje_adicional.set_index('id')
costo_almacenaje_adicional = costo_almacenaje_adicional.set_index('id')
costo_fijo_bodega_adicional =costo_fijo_bodega_adicional.set_index('id')
inventario_inicial_adicional = inventario_inicial_adicional.set_index('id')
capacidad_almacenaje = capacidad_almacenaje.set_index('id')
costo_almacenaje = costo_almacenaje.set_index('id')
costo_produccion = costo_produccion.set_index('id')
inventario_inicial = inventario_inicial.set_index('id')
oferta_max_proveedores = oferta_max_proveedores.set_index('id')
oferta_min_proveedores = oferta_min_proveedores.set_index('id')
demanda_max = demanda_max.set_index('id')
demanda_min = demanda_min.set_index('id')
nodos_produccion = nodos_produccion.set_index('id')
nodos_bodegas = nodos_bodegas.set_index('id')
nodos_demanda = nodos_demanda.set_index('id')
precio_venta = precio_venta.set_index('id')

# Se llena la matriz
'''for i, nodo_i in enumerate(nodos_relevantes):
    for j, nodo_j in enumerate(nodos_relevantes):
        if i != j:
            matriz_distancias[i, j] = nx.shortest_path_length(grafo_vial, source=nodo_i, target=nodo_j, weight='weight')
'''
# Se define la constante de costo por unidad de distancia
c_tte = 1  # Puedes cambiar este valor según sea necesario

# Se calcula la matriz de costos basada en la matriz de distancias
'''matriz_costos = c_tte * matriz_distancias'''

# Se crea un DataFrame de la matriz de costos
'''matriz_costos_df = pd.DataFrame(matriz_costos, index=nodos_relevantes, columns=nodos_relevantes)

# Se muestra la matriz de costos
print("Matriz de Costos de Transporte entre Nodos:")
print(matriz_costos_df)'''