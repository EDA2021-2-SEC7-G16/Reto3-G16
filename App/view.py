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

def printLatestSighting(key, size):
    print('La hora más tardía con avistamientos fue ' + str(key) + ', con ' + str(size) + ' avistamientos.')

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
    print("6- Contar los avistamientos en un rango de fechas")
    print("7- Contar los avistamientos de una zona geografica")

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

def printSightingsByDate(date_inf,date_sup,cont):

    oldest_date, size_oldestdate = controller.oldestdatesighting(cont)

    print('La fecha mas antigua de la cual se tiene avistamientos es : ', oldest_date, ' con un total de avistamientos de: ', size_oldestdate)

    final_trees, sizeSightings  = controller.rangedSightingsBydate(date_inf,date_sup,cont)

    print('Hay ', sizeSightings , ' avistamientos en el rango')

    n = (1,2,3,int(sizeSightings) -2,int(sizeSightings) -1,int(sizeSightings))

    if sizeSightings <= 6:
        for x in lt.iterator(final_trees):
            print(x)
            print('Fecha: ', x['datetime'])
            print('Forma: ',x['shape'])
            print('Pais: ',x['country'])
            print('Ciudad: ',x['city'])
            print('Latitud: ',x['latitude'])
            print('Longitud: ',x['longitude'])
    else:
        for x in n:
            print(x)
            print('Fecha: ', lt.getElement(final_trees,x)['datetime'])
            print('Forma: ', lt.getElement(final_trees,x)['shape'])
            print('Pais: ', lt.getElement(final_trees,x)['country'])
            print('Ciudad: ', lt.getElement(final_trees,x)['city'])
            print('Latitud: ', lt.getElement(final_trees,x)['latitude'])
            print('Longitud: ', lt.getElement(final_trees,x)['longitude'])

def printSightingsByLatitude(latitude_inf,latitude_sup,longitude_inf,longitude_sup,cont):


    final_trees, sizeSightings  = controller.rangedSightingsByposition(latitude_inf,latitude_sup,longitude_inf,longitude_sup,cont)

    print('Hay ', sizeSightings , ' avistamientos en el rango')

              
         

     

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
        
        startTime = process_time()
        printSightingsByDuration(time_inf,time_sup,cont)
        stopTime = process_time()
        execTime = (stopTime - startTime) * 1000
        print('El tiempo de ejecución fue de ' + str(execTime) + ' milisegundos. \n')
    

    elif int(inputs[0]) == 5:
        lowerLimit = input('¿Desde qué hora desea consultar los avistamientos? (formato HH:MM) ')
        upperLimit = input('¿Hasta qué hora desea consultar los avistamientos? (formato HH:MM) ')
        print('\n')
        startTime = process_time()
        answer = controller.sightingsInRange(cont, lowerLimit, upperLimit)
        stopTime = process_time()
        execTime = (stopTime - startTime) * 1000

        print('El tiempo de ejecución fue de ' + str(execTime) + ' milisegundos. \n')
        print('Dentro del rango de ' + str(lowerLimit) + ' y ' + str(upperLimit) + ' hubo ' + str(answer[1]) + ' avistamientos.')
        printLatestSighting(answer[2], answer[3])
        size = lt.size(answer[0])
        printFirstThree(answer[0])
        printLastThree(answer[0], size)

    elif int(inputs[0]) == 6:
        date_inf = input('Digite la la fecha inferior en el fomrato AAAA-MM-DD')
        date_sup = input('Digite la la fecha superior en el fomrato AAAA-MM-DD')
        
        startTime = process_time()
        printSightingsByDate(date_inf,date_sup,cont)
        stopTime = process_time()
        execTime = (stopTime - startTime) * 1000
        print('El tiempo de ejecución fue de ' + str(execTime) + ' milisegundos. \n')

    elif int(inputs[0]) == 7:
        longitude_inf = float(input('Digite la longitud minima'))
        longitude_sup = float(input('Digite la longitud maxima'))
        latitude_inf = float(input('Digite la latitud minima'))
        latitude_sup = float(input('Digite la latitud maxima'))
        
         
        printSightingsByLatitude(latitude_inf,latitude_sup,longitude_inf,longitude_sup,cont)

    else:
        sys.exit(0)
sys.exit(0)
