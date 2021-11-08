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
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printUfoData(ufo):
    print('La fecha del avistamiento es ' + ufo['datetime'] + ', en la ciudad de ' + ufo['city'] + ', en el país ' + ufo['country'] + '.')
    print('La duración del avistamiento fue de ' + ufo['duration (seconds)'] + ' segundos, y su forma fue ' + ufo['shape'] + '.\n')

def printFirstFive(tree):
    print('\n Primeros 5 avistamientos: \n')
    for n in range(1, 6):
        printUfoData(lt.getElement(cont['ufos'], n))

def printLastFive(tree, size):
    print('\n Últimos 5 avistamientos: \n')
    for n in range(0, 5):
        printUfoData(lt.getElement(cont['ufos'], (size-n)))

def printMenu():
    print("Bienvenido")
    print("1- Inicializar analizador")
    print("2- Cargar información de avistamientos")

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
        printLastFive(cont['ufos'], mp.size(cont['ufos']))

    else:
        sys.exit(0)
sys.exit(0)
