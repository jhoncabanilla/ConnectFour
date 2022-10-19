import numpy as np

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



# Creamos el tablero
tablero = create_board()

# Mediante el siguiente loop vamos a controlar si la partida ha terminado o no
game_over = False
turno = 0
while not game_over:
    # Entrada del jugador #1
    if turno == 0:
        seleccion = int(input("Jugador 1 -- Seleccione (1-7):"))
        # TODO: meter en un bucle while
        if seleccion < 1 or seleccion > 7:
            print("Columna invalida")
            exit(1)

        tablero, rows = coloca_ficha(tablero, seleccion, turno)

        # Ahora deberemos comprobar si el jugador ha ganado o la partida continua
        game_over = movimiento_ganador(tablero, 1)

        if game_over:
            print("GANA EL JUGADOR #1\n")

    # Entrada del jugador #2
    else:
        seleccion = int(input("Jugador 2 -- Seleccione (1-7):"))
        if seleccion < 1 or seleccion > 7:
            print("Columna invalida")
            exit(1)

        tablero, rows = coloca_ficha(tablero, seleccion, turno)

        # Ahora deberemos comprobar si el jugador ha ganado o la partida continua
        game_over = movimiento_ganador(tablero, 2)

        if game_over:
            print("GANA EL JUGADOR #2\n")
    
    # De esta manera, vamos variando la variable turno entre 0 y 1
    turno += 1
    turno = turno % 2

    print(tablero, "\n")