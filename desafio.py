# -*- coding: latin-1 -*-


import csv
import bisect
import heapq
import sys



class Socio:
    def __init__(self, nombre, edad, equipo, estado_civil, nivel_estudios):
        self.nombre         = nombre
        self.edad           = int(edad)
        self.equipo         = equipo
        self.estado_civil   = estado_civil
        self.nivel_estudios = nivel_estudios

    def __gt__(self, other):
        return self.edad > other.edad

    def __lt__(self, other):
        return self.edad < other.edad

    def __eq__(self, other):
        return self.edad == other.edad

    def universitariosCasados(self):
        return self.estado_civil == "Casado" and self.nivel_estudios == "Universitario"


class Club:
    def __init__(self, socio):
        self.nombre          = socio.equipo
        self.cantidad_socios = 1
        self.promedio_edad   = socio.edad
        self.min_edad        = socio.edad
        self.max_edad        = socio.edad

    def agregarSocio(self, socio):
        if self.nombre == socio.equipo:

            self.promedio_edad = (self.promedio_edad * self.cantidad_socios + socio.edad) / (self.cantidad_socios + 1)
            self.cantidad_socios += 1

            if socio.edad < self.min_edad:
                self.min_edad = socio.edad

            if socio.edad > self.max_edad:
                self.max_edad = socio.edad


# Usando heaps, armo un diccionario con cada nombre y su cantidad de apariciones
# itero nombre por nombre del diccionario de entrada hasta llenar el heap con 5
# elementos. Luego comienzo a evaluar cada vez que un nuevo nombre tenga una cantidad
# de apariciones superior a la cabeza del heap mínimo. 
# Aqui, quito la cabeza y agrego el iterador actual
def nombresComunes(dicc):
    aux_res = []
    heapq.heapify(aux_res)

    for k, v in dicc.items():
        if len(aux_res) < 5:
            heapq.heappush(aux_res, (v, k))
        elif v > aux_res[0][0]:
            heapq.heappushpop(aux_res, (v, k))

    return [nombre[1] for nombre in aux_res]


# Función para mostrar el punto 5 en pantalla. 
def mostrarClubes(clubes):
    largoNombres   = [len(nombre) for nombre in clubes.keys()]
    nombreMasLargo =  max(largoNombres)

    colCantSoc  = "Socios: "
    colEdadProm = "Edad Promedio: "
    colEdadMin  = "Edad mínima: "
    colEdadMax  = "Edad maxima: "
    print("Club:".ljust(nombreMasLargo), colCantSoc, colEdadProm, colEdadMin, colEdadMax)

    for k, v in clubes.items():
        nombreClub   = k.ljust(nombreMasLargo)
        cantSocios   = str(v.cantidad_socios).center(len(colCantSoc))
        edadPromedio = ("%.2f" % v.promedio_edad).center(len(colEdadProm))
        edadMin      = str(v.min_edad).center(len(colEdadMin))
        edadMax      = str(v.max_edad).center(len(colEdadMax))

        print(nombreClub, cantSocios, edadPromedio, edadMin, edadMax)


# Función para mostrar el punto 3 en pantalla (o no) y mandarlo a otro archivo csv o no
# según lo especificado por parámetros.
def mostrarTop100(top100, mostrarTop, archivoSalida):

    if not mostrarTop and not archivoSalida:
        return

    colNombre = "Nombre Socio: "
    colEdad   = "Edad: "
    colEquipo = "Club: "

    print(colNombre, colEdad, colEquipo)

    escritorSalida = False

    if archivoSalida:
        if archivoSalida == "-o":
            archivoSalida = "top100.csv"
        else:
            archivoSalida += ".csv"
        open(archivoSalida, 'w').close()


    for socio in top100:
        nombre = socio.nombre.ljust(len(colNombre))
        edad   = str(socio.edad).center(len(colEdad))
        equipo = socio.equipo.ljust(len(colEquipo))

        if mostrarTop:
            print(nombre, edad, equipo)

        if archivoSalida:
            with open(archivoSalida, "a", encoding='latin-1') as salida:
                escritorSalida = csv.writer(salida, delimiter=';')
                escritorSalida.writerow([socio.nombre, socio.edad, socio.equipo])
                

# Función para mostrar todo en pantalla.
def mostrarData(personasRegistradas, top100, clubes, nombresRiver, mostrarTop, archivoSalida):

    print("---Challenge Superliga---\n\n")
    print("Personas registradas:", personasRegistradas, "\n")
    print("Promedio de edad de los socios de Racing:", "%.2f" % clubes["Racing"].promedio_edad, "\n")
    mostrarTop100(top100, mostrarTop, archivoSalida)
    print()
    mostrarClubes(clubes)
    print()

    print("Los cinco nombres más comunes de los hinchas de river son:")
    for i in range(4):
        print(nombresRiver[i], "\b,", end=" ")
    print("\b\b y", nombresRiver[4])


def main(args):
    personasRegistradas = 0
    top100 = []
    clubes = {}
    nombresRiver = []

    with open('socios.csv', encoding='latin-1') as entrada:
        socios = csv.reader(entrada, delimiter=';')

        nombresRiverTodos = {}

        for fila in socios:
            personasRegistradas += 1

            socio = Socio(fila[0], fila[1], fila[2], fila[3], fila[4]) 

            if socio.equipo in clubes:
                clubes[socio.equipo].agregarSocio(socio)
            else:
                clubes[socio.equipo] = Club(socio)

            if len(top100) < 100 and socio.universitariosCasados():
                bisect.insort(top100, socio)

            if socio.equipo == "River":
                if socio.nombre in nombresRiver:
                    nombresRiverTodos[socio.nombre] += 1
                else:
                    nombresRiverTodos[socio.nombre] = 1

        nombresRiver = nombresComunes(nombresRiverTodos)
    
    mostrarTop    = True
    archivoSalida = False

    if "--sin100" in args:
        mostrarTop = False

    if "-o" in args:
        if len(args) == 3 or "--sin100" not in args:
            archivoSalida = args[1 + args.index("-o")]
        else:
            archivoSalida = "-o"

    mostrarData(personasRegistradas, top100, clubes, nombresRiver, mostrarTop, archivoSalida)



if __name__ == "__main__":
    main(sys.argv[1:])
