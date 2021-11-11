"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from time import process_time
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printUfoData(ufo):
    print('La fecha del avistamiento es ' + str(ufo['datetime']) + ', en la ciudad de ' + ufo['city'] + ', en el país ' + ufo['country'] + '.')
    print('La duración del avistamiento fue de ' + ufo['duration (seconds)'] + ' segundos, y su forma fue ' + ufo['shape'] + '.\n')

def printFirstFive(ufoList):
    print('\nPrimeros 5 avistamientos: \n')
    for n in range(1, 6):
        printUfoData(lt.getElement(ufoList, n))

def printLastFive(ufoList, size):
    print('\nÚltimos 5 avistamientos: \n')
    printUfoData(lt.getElement(ufoList, (size-4)))
    printUfoData(lt.getElement(ufoList, (size-3)))
    printUfoData(lt.getElement(ufoList, (size-2)))
    printUfoData(lt.getElement(ufoList, (size-1)))
    printUfoData(lt.getElement(ufoList, size))

def printFirstThree(ufoList):
    print('\nPrimeros 3 avistamientos: \n')
    for n in range(1, 4):
        printUfoData(lt.getElement(ufoList, n))

def printLastThree(ufoList, size):
    print('Últimos 3 avistamientos: \n')
    printUfoData(lt.getElement(ufoList, (size-2)))
    printUfoData(lt.getElement(ufoList, (size-1)))
    printUfoData(lt.getElement(ufoList, size))

def printMenu():
    print("Bienvenido")
    print("1- Inicializar analizador")
    print("2- Cargar información de avistamientos")
    print("3- Contar los avistamientos en una ciudad")
    print("4- Contar los avistmientos por duracion")
    print("5- Contar avistamientos por hora/minutos del día")

def printSightingsByDuration(time_inf,time_sup,cont):

    maxDuration, sizeMaxDuration = controller.totalSigtingsWitLongestDuration(cont)

    print('La mayor duracion fue de: ', maxDuration, ' con ', sizeMaxDuration, ' avistamientos con esa duracion')

    rangedSightings, sizeSigtings = controller.sightingsByLimitTimes(time_inf,time_sup,cont)

    print('Hay ', sizeSigtings, ' avistamientos en el rango')

    n = (1,2,3,int(sizeSigtings) -2,int(sizeSigtings) -1,int(sizeSigtings))

    if sizeSigtings <= 6:
        for x in lt.iterator(rangedSightings):
            print(x)
            print('Fecha: ', x['datetime'])
            print('Forma: ',x['shape'])
            print('Pais: ',x['country'])
            print('Ciudad: ',x['city'])
            print('Duracion: ',x['duration (seconds)'])
    else:
        for x in n:
            print(x)
            print('Fecha: ', lt.getElement(rangedSightings,x)['datetime'])
            print('Forma: ', lt.getElement(rangedSightings,x)['shape'])
            print('Pais: ', lt.getElement(rangedSightings,x)['country'])
            print('Ciudad: ', lt.getElement(rangedSightings,x)['city'])
            print('Duracion: ', lt.getElement(rangedSightings,x)['duration (seconds)'])

     

cont = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("\nInicializando...")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de avistamientos...")
        controller.loadData(cont)
        print('Avistamientos cargados: ' + str(controller.ufoSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
        print('Menor llave: ' + str(controller.minKey(cont)))
        print('Mayor llave: ' + str(controller.maxKey(cont)))
        printFirstFive(cont['ufos'])
        printLastFive(cont['ufos'], lt.size(cont['ufos']))

    elif int(inputs[0]) == 3:
        city = input('¿Qué ciudad desea consultar? ')
        startTime = process_time()
        answer = controller.sightingsInCity(cont, city)
        stopTime = process_time()
        execTime = (stopTime - startTime) * 1000

        print('El tiempo de ejecución fue de ' + str(execTime) + ' milisegundos. \n')
        print('En ' + str(answer[0]) + ' distintas ciudades, ha habido registro de avistamientos.')
        print('En la ciudad de ' + city + ', hubo un total de ' + str(answer[1]) + ' avistamientos. \n')
        printFirstThree(answer[2])
        printLastThree(answer[2], lt.size(answer[2]))

    elif int(inputs[0]) == 4:
        time_inf = input('Digite la duracion en segundos desde la que desea consultar')
        time_sup = input('Digite la duracion en segundos hasta la que desea consultar')
        time_inf = float(time_inf) 
        time_sup = float(time_sup) 
        printSightingsByDuration(time_inf,time_sup,cont)
        
    

    elif int(inputs[0]) == 5:
        lowerLimit = input('¿Desde qué hora desea consultar los avistamientos? (formato HH:MM) ')
        upperLimit = input('¿Hasta qué hora desea consultar los avistamientos? (formato HH:MM) ')
        print('\n')
        startTime = process_time()
        answer = controller.sightingsInRange(cont, lowerLimit, upperLimit)
        stopTime = process_time()
        execTime = (stopTime - startTime) * 1000

        print('El tiempo de ejecución fue de ' + str(execTime) + ' milisegundos.')
        print('Dentro del rango de ' + str(lowerLimit) + ' y ' + str(upperLimit) + ' hubo ' + str(answer[1]) + ' avistamientos.')
        size = lt.size(answer[0])
        printFirstThree(answer[0])
        printLastThree(answer[0], size)

    else:
        sys.exit(0)
sys.exit(0)
