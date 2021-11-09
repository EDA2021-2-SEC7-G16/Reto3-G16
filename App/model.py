"""
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from time import strptime
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as merge
import datetime
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los avistamientos
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'ufos': None,
                'dateIndex': None,
                'cityIndex': None,
                'sightingsIndex': None}

    analyzer['ufos'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='BST',
                                      comparefunction=compareDates)
    analyzer['cityIndex'] = om.newMap(omaptype='RBT')
    analyzer['sightingsIndex'] = om.newMap(omaptype='RBT')

    return analyzer

# Funciones para agregar informacion al catalogo

def addUfo(analyzer, ufo):
    """
    """
    lt.addLast(analyzer['ufos'], ufo)
    updateDateIndex(analyzer['dateIndex'], ufo)
    return analyzer

def addSightingsPerCity(analyzer, ufo):
    citiesTree = analyzer['cityIndex']
    sightingInfo = relevantInfo(ufo)
    city = ufo['city']
    entry = om.get(citiesTree, city)

    if entry is None:
        cityInfo = om.newMap()
        om.put(cityInfo, sightingInfo['datetime'], sightingInfo)
        om.put(citiesTree, city, cityInfo)
    else:
        cityInfo = me.getValue(entry)
        om.put(cityInfo, sightingInfo['datetime'], sightingInfo)

def addSightingTimes(analyzer, ufo):
    sightingsTree = analyzer['sightingsIndex']
    sightingInfo = relevantInfo(ufo)
    time = datetime.datetime.strftime(sightingInfo['datetime'], '%H:%M')
    entry = om.get(sightingsTree, time)

    if entry is None:
        timeInfo = om.newMap()
        om.put(timeInfo, sightingInfo['datetime'], ufo)
        om.put(sightingsTree, time, timeInfo)
    else:
        timeInfo = me.getValue(entry)
        om.put(timeInfo, sightingInfo['datetime'], ufo)

def updateDateIndex(map, ufo):
    """
    Se toma la fecha del avistamiento y se busca si ya existe en el arbol
    de dicha fecha.  Si es asi, se adiciona a su lista de avistamientos
    y se actualiza el indice de tipos de avistamientos.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de avistamientos
    """
    occurreddate = ufo['datetime']
    ufodate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, ufodate.date())
    if entry is None:
        datentry = newDataEntry(ufo)
        om.put(map, ufodate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, ufo)
    return map

def newDataEntry(ufo):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'shapeIndex': None, 'lstufos': None}
    entry['shapeIndex'] = mp.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareShapes)
    entry['lstufos'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def addDateIndex(datentry, ufo):
    """
    Actualiza un indice de tipo de avistamientos.  Este indice tiene una lista
    de avistamientos y una tabla de hash cuya llave es el tipo de avistamiento y
    el valor es una lista con los avistamientos de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstufos']
    lt.addLast(lst, ufo)
    shapeIndex = datentry['shapeIndex']
    ufoentry = mp.get(shapeIndex, ufo['shape'])
    if (ufoentry is None):
        entry = newShapeEntry(ufo['shape'], ufo)
        lt.addLast(entry['lstufos'], ufo)
        mp.put(shapeIndex, ufo['shape'], entry)
    else:
        entry = me.getValue(ufoentry)
        lt.addLast(entry['lstufos'], ufo)
    return datentry

def newShapeEntry(shapegrp, ufo):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    spentry = {'shape': None, 'lstufos': None}
    spentry['shape'] = shapegrp
    spentry['lstufos'] = lt.newList('SINGLELINKED', compareShapes)
    return spentry

# Funciones para creacion de datos

def relevantInfo(ufo):
    dateTime = ufo['datetime']
    dateTime = datetime.datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')

    relevantData = {'datetime': dateTime,
                    'shape': ufo['shape'],
                    'country': ufo['country'],
                    'city': ufo['city'],
                    'duration (seconds)': ufo['duration (seconds)']}
    return relevantData

# Funciones de consulta

def ufoSize(analyzer):
    """
    Número de avistamientos
    """
    return lt.size(analyzer['ufos'])

def indexHeight(analyzer):
    """
    Altura del arbol
    """
    return om.height(analyzer['dateIndex'])

def indexSize(analyzer):
    """
    Numero de elementos en el indice
    """
    return om.size(analyzer['dateIndex'])

def minKey(analyzer):
    """
    Llave mas pequena
    """
    return om.minKey(analyzer['dateIndex'])

def maxKey(analyzer):
    """
    Llave mas grande
    """
    return om.maxKey(analyzer['dateIndex'])

def sightingsInCity(analyzer, city):
    citiesMap = analyzer['cityIndex']
    entry = om.get(citiesMap, city)
    sightingsTree = me.getValue(entry)

    firstLastThree = lt.newList('ARRAY_LIST')
    sightingsAmmount = om.size(sightingsTree)
    citiesSightings = om.size(citiesMap)

    addFirstThree(sightingsTree, firstLastThree)
    addLastThree(sightingsTree, firstLastThree)
    firstLastThree = merge.sort(firstLastThree, compareTime)

    return citiesSightings, sightingsAmmount, firstLastThree

def addFirstThree(tree, returnList):
    treeSize = om.size(tree)
    lowerKey = om.minKey(tree)

    if treeSize >= 3:
        upperKey = om.select(tree, 2)
    else:
        upperKey = om.maxKey(tree)

    elementSet = om.values(tree, lowerKey, upperKey)
    setSize = lt.size(elementSet)

    pos = 1
    while pos <= setSize:
        sighting = lt.getElement(elementSet, pos)
        lt.addLast(returnList, sighting)
        pos += 1

def addLastThree(tree, returnList):
    treeSize = om.size(tree)

    if treeSize >= 6:
        lowerKey = om.select(tree, (treeSize - 3))
        upperKey = om.maxKey(tree)
    elif (treeSize > 3) and (treeSize < 6):
        lowerKey = om.select(tree, 3)
        upperKey = om.maxKey(tree)

    if treeSize > 3:
        elementSet = om.values(tree, lowerKey, upperKey)
        setSize = lt.size(elementSet)
        pos = 1

        while pos <= setSize:
            sighting = lt.getElement(elementSet, pos)
            lt.addLast(returnList, sighting)
            pos += 1

def sightingsInRange(analyzer, lowerLimit, upperLimit):
    sightingsTree = analyzer['sightingsIndex']
    sightings = om.values(sightingsTree, lowerLimit, upperLimit)
    returnList = lt.newList('ARRAY_LIST')
    sightingsSize = lt.size(sightings)
    pos = 1

    while pos <= sightingsSize:
        subTree = lt.getElement(sightings, pos)
        subList = om.valueSet(subTree)
        subLSize = lt.size(subList)
        n = 1

        while n <= subLSize:
            sighting = lt.getElement(subList, n)
            lt.addLast(returnList, sighting)
            n +=1
        pos += 1

    sightingsAmmount = lt.size(returnList)
    returnList = merge.sort(returnList, compareHourTime)

    return returnList, sightingsAmmount

# Funciones utilizadas para comparar elementos dentro de una lista

def compareIds(id1, id2):
    """
    Compara dos avistamientos
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareTime(ufo1, ufo2):
    d1 = datetime.datetime.strptime(str(ufo1['datetime']), '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(str(ufo2['datetime']), '%Y-%m-%d %H:%M:%S')
    return d1 < d2

def compareHourTime(ufo1, ufo2):
    d1 = datetime.datetime.strptime(ufo1['datetime'], '%Y-%m-%d %H:%M:%S')
    d1 = datetime.datetime.strftime(d1, '%H:%M')
    d2 = datetime.datetime.strptime(ufo2['datetime'], '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strftime(d2, '%H:%M')
    return d1 < d2

def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareShapes(shape1, shape2):
    """
    Compara dos tipos de avistamientos
    """
    shape = me.getKey(shape2)
    if (shape1 == shape):
        return 0
    elif (shape1 > shape):
        return 1
    else:
        return -1


# Funciones de ordenamiento
