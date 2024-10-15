import funciones as func
from abc import ABC, abstractmethod
from parametros import FELICIDAD_ADICIONAL_DOCENCIO, FELICIDAD_PERDIDA_TAREO,\
      ENERGIA_PERDIDA_DOCENCIO, EDAD_ADICIONAL_TAREO, SUERTE_ADICIONAL_TAREO,\
          FUERZA_ADICIONAL_DOCENCIO, FELICIDAD_PERDIDA
import networkx as nx

class Nodo(ABC):
    def __init__(self, nodo: nx.Node) -> None:
        self.id = nodo[0]
        self.y = nodo[0][1]['pos'][0]
        self.x = nodo[0][1]['pos'][1]
        self.tipo = nodo[0][1]['tipo']
        self.nodo = nodo
        self._edad = int(caracteristicas[2])
        self._energia = int(caracteristicas[3])
        self._fuerza = int(caracteristicas[4])
        self._suerte = int(caracteristicas[5])
        self._felicidad = int(caracteristicas[6])
        self.tipo = caracteristicas[1]
        self.metros_cavados = 0
        
        self.dias_que_se_necesita_descansar = 0
        self.dias_descansados = 0
        self.descansando = False
        self.encontro_un_item = False
        self.encontrado = []

    @property
    def energia(self):
        return self._energia
    
    @energia.setter
    def energia(self, var):
            self._energia = min(100, max(var, 0))

    @property
    def edad(self):
        return self._edad
    
    @edad.setter
    def edad(self, e):
        if e < 18:
            self._edad = 18
        elif e > 60:
            self._edad = 60
        else:
            self._edad = e

    @property
    def felicidad(self):
        return self._felicidad
    
    @felicidad.setter
    def felicidad(self, e):
        self._felicidad = min(max(e, 1), 10)


    @property
    def fuerza(self):
        return self._fuerza
    
    @fuerza.setter
    def fuerza(self, e):
        if e < 1:
            self._fuerza = 1
        elif e > 10:
            self._fuerza = 10
        else:
            self._fuerza = e

    @property
    def suerte(self):
        return self._suerte
    
    @suerte.setter
    def suerte(self, e):
        if e < 1:
            self._suerte = 1
        elif e > 10:
            self._suerte = 10
        else:
            self._suerte = e

    def descansar(self):
        dias_descanso = int(self._edad / 20)
        self.dias_que_se_necesita_descansar = dias_descanso
        self.descansando = True        

    def encontrar_item(self):
        item_encontrado = func.encontrar_itemes(self._suerte)
        if item_encontrado != None:
            self.encontrado = item_encontrado
            self.encontro_un_item = True

    @abstractmethod
    def gastar_energia(self):
        energia_perdida = int((10 / self._fuerza) + (self._edad / 6))
        self.energia -= energia_perdida
        return self.energia

    @abstractmethod
    def cavar(self, dificultad):
        self.metros_cavados = round(((30 / (self._edad + self.felicidad)) + \
                                     (2 * self._fuerza / 10)) * (1 / (10 * dificultad)), 2)
        self.gastar_energia()
        self.encontrar_item()
            
    @abstractmethod
    def consumir(self, a_consumir: list):

        self.energia += int(a_consumir[4])
        self.fuerza += int(a_consumir[5])
        self.suerte += int(a_consumir[6])
        self.felicidad += int(a_consumir[7])
    
    @abstractmethod
    def perder_por_evento(self):
        self.felicidad -= FELICIDAD_PERDIDA

class Bodega(Nodo):
    def __init__(self, , ,
                 c_almacenaje, cap_inv_max, ) -> None:
        super().__init__(self, nodo, c_almacenaje, cap_inv_max, inv_inicial)

    def cavar(self, dificultad):
        self.edad += EDAD_ADICIONAL_TAREO
        self.felicidad -= FELICIDAD_PERDIDA_TAREO
        super().cavar(dificultad)
    
    def consumir(self, a_consumir):
        self.suerte += SUERTE_ADICIONAL_TAREO
        super().consumir(a_consumir)
    
    def descansar(self):
        return super().descansar()

    def gastar_energia(self):
        return super().gastar_energia()

    def perder_por_evento(self, *args, **kwargs):
        return super().perder_por_evento(*args, **kwargs)

class Produccion(Nodo):
    def __init__(self, cap_prod_max, cap_prod_min, nodo, 
                 c_almacenaje, cap_inv_max, inv_inicial) -> None:
        super().__init__(self, nodo, c_almacenaje, cap_inv_max, inv_inicial)


    @property
    def energia(self):
        return self._energia
    
    @energia.setter
    def energia(self, valor):
        self._energia = min(100, max(valor, 20))

    def cavar(self, dificultad):
        return super().cavar(dificultad)
    
    def consumir(self, a_consumir):
        return super().consumir(a_consumir)

    def gastar_energia(self):
        energia_perdida = int(((10 / self._fuerza) + (self._edad / 6)) / 2)
        self.energia -= energia_perdida

        return self.energia

    def perder_por_evento(self, *args, **kwargs):
        return super().perder_por_evento(*args, **kwargs)
class Demanda(Nodo):   
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def cavar(self, dificultad):
        self.felicidad += FELICIDAD_ADICIONAL_DOCENCIO
        self.fuerza += FUERZA_ADICIONAL_DOCENCIO
        super().cavar(dificultad)

    def descansar(self):
        return super().descansar()

    def gastar_energia(self):
        self.energia -= ENERGIA_PERDIDA_DOCENCIO
        return self._energia
    
    def consumir(self, a_consumir, *args, **kwargs):
        return super().consumir(a_consumir, *args, **kwargs)
    
    def perder_por_evento(self, *args, **kwargs):
        return super().perder_por_evento(*args, **kwargs)