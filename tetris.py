import pygame
import random

# Inicialización de pygame
pygame.init()

# Dimensiones de la pantalla
ancho_pantalla = 800
alto_pantalla = 600

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
NARANJA = (255, 165, 0)

# Tamaño de cada bloque del Tetris
tamano_bloque = 30

# Crear la pantalla del juego
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("Tetris")

# Reloj para controlar la velocidad de actualización de la pantalla
reloj = pygame.time.Clock()

# Clase para manejar las piezas del Tetris
class Pieza:
    def __init__(self, forma, color):
        self.forma = forma
        self.color = color
        self.x = ancho_pantalla // 2 - len(forma[0]) // 2
        self.y = 0
    
    def mover_abajo(self):
        self.y += 1
    
    def mover_izquierda(self):
        self.x -= 1
    
    def mover_derecha(self):
        self.x += 1
    
    def mover_arriba(self):
        self.y -= 1

    def girar(self):
        self.forma = list(zip(*reversed(self.forma)))
    
    def dibujar(self):
        for i in range(len(self.forma)):
            for j in range(len(self.forma[i])):
                if self.forma[i][j] == "X":
                    pygame.draw.rect(pantalla, self.color, (self.x * tamano_bloque + j * tamano_bloque, self.y * tamano_bloque + i * tamano_bloque, tamano_bloque, tamano_bloque))
                    pygame.draw.rect(pantalla, NEGRO, (self.x * tamano_bloque + j * tamano_bloque, self.y * tamano_bloque + i * tamano_bloque, tamano_bloque, tamano_bloque), 1)
    
    def colision(self, tablero):
        for i in range(len(self.forma)):
            for j in range(len(self.forma[i])):
                if self.forma[i][j] == "X":
                    if self.y + i >= len(tablero) or self.x + j < 0 or self.x + j >= len(tablero[0]) or tablero[self.y + i][self.x + j] != ".":
                        return True
        return False

# Crear una lista de formas de las piezas del Tetris
formas = [
    [["X", "X", "X", "X"]],
    [["X", "X"], ["X", "X"]],
    [["X", "X", "X"], [".", ".", "X"]],
    [["X", "X", "X"], ["X", ".", "."]],
    [["X", "X", "X"], [".", "X", "."]],
    [["X", "X", "."], [".", "X", "X"]],
    [[".", "X", "X"], ["X", "X", "."]]
]
# Crear una lista de colores para las piezas
colores = [ROJO, VERDE, AZUL, AMARILLO, CYAN, MAGENTA, NARANJA]

# Función para crear una nueva pieza aleatoria
def nueva_pieza():
    forma = random.choice(formas)
    color = random.choice(colores)
    return Pieza(forma, color)

# Crear el tablero del juego
tablero = []
for i in range(alto_pantalla // tamano_bloque):
    fila = []
    for j in range(ancho_pantalla // tamano_bloque):
        fila.append(".")
        tablero.append(fila)

# Variables para controlar el juego
pieza_actual = nueva_pieza()
tiempo_pieza = 0
tiempo_total = 0
puntaje = 0
game_over = False

# Bucle principal del juego
while not game_over:
# Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            game_over = True
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                pieza_actual.mover_izquierda()
                if pieza_actual.colision(tablero):
                    pieza_actual.mover_derecha()
            elif evento.key == pygame.K_RIGHT:
                pieza_actual.mover_derecha()
                if pieza_actual.colision(tablero):
                    pieza_actual.mover_izquierda()
            elif evento.key == pygame.K_UP:
                pieza_actual.girar()
                if pieza_actual.colision(tablero):
                    pieza_actual.girar()
            elif evento.key == pygame.K_DOWN:
                pieza_actual.mover_abajo()
                if pieza_actual.colision(tablero):
                    pieza_actual.mover_arriba()
    # Actualización del juego
    tiempo_pieza += reloj.tick(60)
    tiempo_total += tiempo_pieza
    if tiempo_pieza > 1000:
        pieza_actual.mover_abajo()
        if pieza_actual.colision(tablero):
            pieza_actual.mover_arriba()
            for i in range(len(pieza_actual.forma)):
                for j in range(len(pieza_actual.forma[i])):
                    if pieza_actual.forma[i][j] == "X":
                        tablero[pieza_actual.y + i][pieza_actual.x + j] = "X"
            filas_completas = 0
            for i in range(len(tablero)):
                if "." not in tablero[i]:
                    filas_completas += 1
                    del tablero[i]
                    tablero.insert(0, [".", ".", ".", ".", ".", ".", ".", ".", ".", "."])
            puntaje += filas_completas * 100
            pieza_actual = nueva_pieza()
            if pieza_actual.colision(tablero):
                game_over = True
        tiempo_pieza = 0

    # Dibujar la pantalla del juego
    pantalla.fill(BLANCO)
    for i in range(len(tablero)):
        for j in range(len(tablero[i])):
            if tablero[i][j] == "X":
                pygame.draw.rect(pantalla, NEGRO, (j * tamano_bloque, i * tamano_bloque, tamano_bloque, tamano_bloque))
                pygame.draw.rect(pantalla, colores[random
    .randint(0, 6)], (j * tamano_bloque + 1, i * tamano_bloque + 1, tamano_bloque - 2, tamano_bloque - 2))
    pieza_actual.dibujar()
    pygame.display.flip()

# Mostrar el puntaje final
print("¡Juego terminado!")
print("Puntaje final:", puntaje)

pygame.quit()