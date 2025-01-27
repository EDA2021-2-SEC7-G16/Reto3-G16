﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos

def loadData(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    ufosfile = cf.data_dir + 'UFOS-utf8-5pct.csv'
    input_file = csv.DictReader(open(ufosfile, encoding="utf-8"),
                                delimiter=",")
    for ufo in input_file:
        model.addUfo(analyzer, ufo)
        model.addSightingsPerCity(analyzer, ufo)
        model.addSightingTimes(analyzer, ufo)
        model.addSigtingDuration(analyzer,ufo)
        model.addSigtingDatess(analyzer,ufo)
        model.addSigtingLatitudes(analyzer,ufo)
    return analyzer

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def ufoSize(analyzer):
    """
    Numero de avistamientos leidos
    """
    return model.ufoSize(analyzer)


def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer)


def indexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer)


def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)


def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)

def sightingsInCity(analyzer, city):
    return model.sightingsInCity(analyzer, city)

def sightingsInRange(analyzer, lowerLimit, upperLimit):
    return model.sightingsInRange(analyzer, lowerLimit, upperLimit)

def totalSigtingsWitLongestDuration(cont):

    cont = cont["durationIndex"]

    return model.totalSigtingsWitLongestDuration(cont)
    
def oldestdatesighting(cont):

    cont = cont["datessIndex"]

    return model.oldestdatesighting(cont)    
    
def sightingsByLimitTimes(time_inf,time_sup,cont):

    cont = cont["durationIndex"]

    return model.sightingsByLimitTimes(time_inf,time_sup,cont)

def rangedSightingsBydate(date_inf,date_sup,cont):

    cont = cont["datessIndex"]

    return model.rangedSightingsBydate(date_inf,date_sup,cont)    

def rangedSightingsByposition(latitude_inf,latitude_sup,longitude_inf,longitude_sup,cont):

    cont = cont["latitudeIndex"]

    return model.rangedSightingsByposition(latitude_inf,latitude_sup,longitude_inf,longitude_sup,cont)   
