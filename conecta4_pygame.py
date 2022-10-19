
import math
import sys

import numpy as np
# SEGUNDA PARTE -- pygame
import pygame

#VARIABLES GLOBALES
FILAS = 6
COLUMNAS = 7
AZUL = (0,0,255)
NEGRO = (0,0,0)
ROJO = (255,0,0)
AMARILLO = (255,255,0)

"Para representar el tablero utilizaremos una matriz de 6 filas y 7 columnas"
def create_board():
    tablero = np.zeros((6,7))
    return tablero


"Funcion que coloca la ficha del jugador en la posicion indicada comprobando dicha posicion"
def coloca_ficha(tablero, seleccion, turno):

    # Lo primero que hacemos es comprobar si en la casilla no hay una ficha previa
    valida, rows = es_valida(tablero, seleccion)

    if valida:
        if turno == 0:
            # Las fichas del jugador #1 tendran el id = 1
            tablero[rows-1][seleccion-1] = 1

        else:
            # Las fichas del jugador #2 tendran el id = 2
            tablero[rows-1][seleccion-1] = 2

    return tablero, rows

"Funcion que comprueba si en la casilla seleccionada se puede colocar una ficha o no"
def es_valida(tablero, seleccion):
    check = True
    rows,_ = tablero.shape

    if tablero[rows-1][seleccion-1] != 0:
        check = False
    else:
        return check, rows

    # En el caso de que la posicion este ocupada, comprobamos las filas superiores buscando alguna casillas vacia hasta llegar a la ultima fila
    if not check:
        # Se podria utilizar un bucle for also! :)
        while tablero[rows-1][seleccion-1] != 0:
            rows -= 1
            # En este caso, la columna estara ocupada por lo que no se permiten nuevas casillas
            if rows == 0:
                return False, rows

        return True, rows

"Funcion que comprueba una jugada ganadora que finalice la partida"
def movimiento_ganador(tablero, num_ficha):
    # Para implementar esta funcion lo que vamos a hacer consiste en ir recorriendo el tablero y comprobar si hay alguna jugada que finalice el juego. No es la manera
    # mas eficaz, ya que seria ir comprobando alrededor de la ficha actual, pero de primeras vamos a implementarlo de esta manera.

    # Filas y columnas
    rows, columns = tablero.shape

    # Caso horizantal: Recorremos hasta la 4º columna, ya que a partir de esta no se pueden dar 4 fichas consecutivas iguales
    for i in range(rows):
        for j in range(columns-3):
            if tablero[i][j] == num_ficha and tablero[i][j+1] == num_ficha and tablero[i][j+2] == num_ficha and tablero[i][j+3] == num_ficha:
                return True
   
   
    # Caso horizantal: Recorremos hasta la 3º fila, ya que a partir de esta no se pueden dar 4 fichas consecutivas iguales
    for j in range(columns):
         for i in range(rows-3):
            if tablero[i][j] == num_ficha and tablero[i+1][j] == num_ficha and tablero[i+2][j] == num_ficha and tablero[i+3][j] == num_ficha:
                return True

    
    # Caso diagonal pendiente negativa: En este caso, recorremos hasta la 4º columna y 3º fila
    for i in range(rows-3):
        for j in range(columns-3):
            if tablero[i][j] == num_ficha and tablero[i+1][j+1] == num_ficha and tablero[i+2][j+2] == num_ficha and tablero[i+3][j+3] == num_ficha:
                return True


    # Caso diagonal pendiente positiva:
    for i in range(3,rows):
        for j in range(columns-3):
            if tablero[i][j] == num_ficha and tablero[i-1][j+1] == num_ficha and tablero[i-2][j+2] == num_ficha and tablero[i-3][j+3] == num_ficha:
                return True


# Funcion mediante la cual se implementa el diseño de la interfaz
def dibuja_tablero(tablero, tam_circulo, radio):

    for i in range(FILAS):
        for j in range(COLUMNAS):
            # Dibujamos un rectangulo azul que represente el tablero y despues dibujamos los circulos correspondientes
            pygame.draw.rect(Screen, AZUL, (j*tam_circulo, i*tam_circulo+tam_circulo, tam_circulo, tam_circulo))

            # En este caso, no hay ninguna ficha colocada -> Circulo negro (vacio)
            if tablero[i][j] == 0:
                pygame.draw.circle(Screen, NEGRO, (int(j*tam_circulo + tam_circulo/2), int(i*tam_circulo + tam_circulo + tam_circulo/2)), radio)

            # En este caso, el jugador 1 coloca ficha, por lo que dibujamos el circulo de color rojo
            elif tablero[i][j] == 1:   
                # Dibujo de los circulos
                pygame.draw.circle(Screen, ROJO, (int(j*tam_circulo + tam_circulo/2), int(i*tam_circulo + tam_circulo + tam_circulo/2)), radio)

            # En este caso, el jugador 2 coloca ficha, por lo que dibujamos el circulo de color amarillo
            else:
                pygame.draw.circle(Screen, AMARILLO, (int(j*tam_circulo + tam_circulo/2), int(i*tam_circulo + tam_circulo + tam_circulo/2)), radio)

    pygame.display.update()


# Creamos el tablero
tablero = create_board()

# Mediante el siguiente loop vamos a controlar si la partida ha terminado o no
game_over = False
turno = 0
filas, columnas = tablero.shape

# Inicializamos el pygame
pygame.init()

# Elementos
tam_circulo = 100 #100 px
width = columnas * tam_circulo
height = (filas+1) * tam_circulo #Fila adicional donde se muestra la ficha antes de ser colocada

size = (width, height)

radio = int(tam_circulo/2 - 5)

Screen = pygame.display.set_mode(size)

dibuja_tablero(tablero, tam_circulo, radio)
pygame.display.update()

texto = pygame.font.SysFont("monospace", 60)

while not game_over:

    for event in pygame.event.get():
        # Cierre de la ventana
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            # Para evitar que todo el rectangulo superior se quede rojo o amarillo, lo que hacemos es dibujar de nuevo un rectangulo
            pygame.draw.rect(Screen, NEGRO, (0, 0, width, tam_circulo))
            posx = event.pos[0]

            if turno == 0:
                pygame.draw.circle(Screen, ROJO, (posx, int(tam_circulo/2)), radio)
            else:
                pygame.draw.circle(Screen, AMARILLO, (posx, int(tam_circulo/2)), radio)

        pygame.display.update()



        # Ahora, ya no necesitamos pedirle a los usuarios que inserten una entreda. Luego mediante el evento click del raton, colocaremos las fichas en la columna 
        # que se haya indicado
        if event.type == pygame.MOUSEBUTTONDOWN:

            # Entrada del jugador #1
            if turno == 0:
                #Obtenemos la posicion x del tablero
                posx = event.pos[0] #Este valor se encuentra entre 1 y 700

                #Como en el problema original pediamos al usuario un valor entre 1-7, ahora para mantener esa dinamica lo que hacemos es sumar
                #a la variable una unidad para ambos turnos
                seleccion = int(math.floor(posx/tam_circulo)) +1 #Redondeo mediante math.floor
             
                tablero, rows = coloca_ficha(tablero, seleccion, turno)

                # Ahora deberemos comprobar si el jugador ha ganado o la partida continua
                game_over = movimiento_ganador(tablero, 1)

                if game_over:
                    pygame.draw.rect(Screen, NEGRO, (0, 0, width, tam_circulo))
                    label1 = texto.render("GANA EL JUGADOR #1", 1, ROJO)
                    Screen.blit(label1, (40,10))

            # Entrada del jugador #2
            else:
                posx = event.pos[0] #Este valor se encuentra entre 0 y 700
                seleccion = int(math.floor(posx/tam_circulo)) + 1
                
                tablero, rows = coloca_ficha(tablero, seleccion, turno)

                # Ahora deberemos comprobar si el jugador ha ganado o la partida continua
                game_over = movimiento_ganador(tablero, 2)

                if game_over:
                    pygame.draw.rect(Screen, NEGRO, (0, 0, width, tam_circulo))
                    label2 = texto.render("GANA EL JUGADOR #2", 1, AMARILLO)
                    Screen.blit(label2, (40,10))
            
            # De esta manera, vamos variando la variable turno entre 0 y 1
            turno += 1
            turno = turno % 2

            print(tablero, "\n")
            dibuja_tablero(tablero, tam_circulo, radio)

            # Cuando la partida haya terminado, implementamos una espera para mostrar un texto referido al jugador ganador
            if game_over:
                pygame.time.wait(4500)