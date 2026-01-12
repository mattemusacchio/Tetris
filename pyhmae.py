import pygame
import random

pygame.init()

# Dimensiones de la pantalla
ancho_pantalla = 600
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
ROSA = (255, 192, 203)
VERDEOSCURO = (0, 100, 0)
ROSA = (255, 192, 203)
VERDEOSCURO = (0, 100, 0)

# Tamaño de cada bloque del Tetris
tamano_bloque = 30

# Crear la pantalla del juego
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("Tetris")

# Reloj para controlar la velocidad de actualización de la pantalla
reloj = pygame.time.Clock()
class Pieza:
    def __init__(self, forma, color):
        self.forma = forma
        self.color = color
        self.x = ancho_pantalla // 2 - len(forma[0]) // 2
        self.y = 0
    
    def mover_abajo(self):
        self.y += 30
    
    def mover_izquierda(self):
        self.x -= 30
    
    def mover_derecha(self):
        self.x += 30
    
    def mover_arriba(self):
        self.y -= 30

    def girar(self):
        self.forma = list(zip(*reversed(self.forma)))

    def dibujar(self):
        for i in range(len(self.forma)):
            for j in range(len(self.forma[i])):
                if self.forma[i][j] == "X":
                    print("hola")
                    #pygame.draw.rect(pantalla, pieza_actual.color, (pieza_actual.x,pieza_actual.y,tamano_bloque*(len(pieza_actual.forma[0])),tamano_bloque*len(pieza_actual.forma)))
                    pygame.draw.rect(pantalla, self.color, (self.x + j * tamano_bloque, self.y + i * tamano_bloque, tamano_bloque, tamano_bloque))
    def colision(self, tablero):
                if len(self.forma) == 1:
                    if self.y >= alto_pantalla:
                        self.mover_arriba()
                        return 4
                else:
                    if (self.y + 60) >= alto_pantalla:
                        self.mover_arriba()
                        return 4
                if self.x >= 590:
                    self.mover_izquierda()
                if self.x <= -90:
                    self.mover_derecha() 

tablero = []
for i in range(alto_pantalla // tamano_bloque):
    fila = []
    for j in range(ancho_pantalla // tamano_bloque):
        fila.append(".")
        tablero.append(fila)

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

def nueva_pieza():
    forma = random.choice(formas)
    color = random.choice(colores)
    print(forma)
    return Pieza(forma, color)

tiempo_pieza = 0
tiempo_total = 0
tiempo = 1000
game_over = False
pieza_actual = nueva_pieza()
# pieza_actual = Pieza([["X", "X", "X", "X"]],AZUL)

while not game_over:
    pantalla.fill(NEGRO)
    for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                game_over = True
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    pieza_actual.mover_izquierda()
                elif evento.key == pygame.K_RIGHT:
                    pieza_actual.mover_derecha()
                elif evento.key == pygame.K_UP:
                    pieza_actual.girar()
                elif evento.key == pygame.K_DOWN:
                    pieza_actual.mover_abajo()
    tiempo_pieza += reloj.tick(60)
    tiempo_total += tiempo_pieza
    if tiempo_pieza > tiempo:
        pieza_actual.mover_abajo()
        if pieza_actual.y + 30 >= alto_pantalla or pieza_actual.x >= 590 or pieza_actual.x <= -90:
            if pieza_actual.colision(tablero) == 4:
                pieza_actual = nueva_pieza()
            pieza_actual.colision(tablero)
        tiempo += 1000
    pieza_actual.dibujar()
    """    
    suma = 0
    for i in pieza_actual.forma[0]:
        if i == ".":
            suma += 1
    #pygame.draw.rect(pantalla, NEGRO, (j * tamano_bloque, i * tamano_bloque, tamano_bloque, tamano_bloque))
    if len(pieza_actual.forma) == 1:
        pygame.draw.rect(pantalla, pieza_actual.color, (pieza_actual.x,pieza_actual.y,tamano_bloque*(len(pieza_actual.forma[0])),tamano_bloque*len(pieza_actual.forma)))
    else:
        suma2 = 0
        for i in pieza_actual.forma[1]:
            if i == ".":
                suma2 += 1
        suma4 = 0
        for i in pieza_actual.forma[0]:
            if i == ".":
                suma4 += 1
            if i == "X":
                break
        suma3 = 0
        for i in pieza_actual.forma[1]:
            if i == ".":
                suma3 += 1
            if i == "X":
                break
        pygame.draw.rect(pantalla, pieza_actual.color, (pieza_actual.x + suma4*tamano_bloque,pieza_actual.y,tamano_bloque*(len(pieza_actual.forma[0]) - suma),tamano_bloque))
        pygame.draw.rect(pantalla, pieza_actual.color, (pieza_actual.x + suma3*tamano_bloque,pieza_actual.y + tamano_bloque,tamano_bloque*(len(pieza_actual.forma[1]) - suma2),tamano_bloque))
    """
    pygame.display.flip()
pygame.display.flip()

