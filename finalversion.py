import pygame
import random
import csv

# Inicialización de pygame
pygame.init()

# Dimensiones de la pantalla
ancho_pantalla = 800
alto_pantalla = 600

# Colores
GRIS = (36, 38, 36)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 64, 54)
VERDE = (17, 173, 67)
AZUL = (54, 71, 224)
AMARILLO = (255, 255, 0)
CYAN = (16, 165, 179)
MAGENTA = (223, 60, 232)
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
                    pygame.draw.rect(pantalla, self.color, (self.x + j * tamano_bloque, self.y + i * tamano_bloque, tamano_bloque, tamano_bloque))
                    pygame.draw.rect(pantalla, NEGRO, (self.x + j * tamano_bloque, self.y + i * tamano_bloque, tamano_bloque, tamano_bloque), 1)
    def colision(self,tablero):
        for i in range(len(self.forma)):
            for j in range(len(self.forma[i])):
                if self.forma[i][j] == "X":
                    if self.y + i*tamano_bloque >= alto_pantalla or self.x + j*tamano_bloque < 0 or self.x + j*tamano_bloque > 780 or tablero[(pieza_actual.y//tamano_bloque)+i][(pieza_actual.x//tamano_bloque)+j] != ".":
                        return True
        return False

class PiezaVieja:
    def __init__(self,forma, color, x, y):
        self.forma = forma
        self.color = color
        self.x = x
        self.y = y

    def dibujar(self):
        for i in range(len(self.forma)):
            for j in range(len(self.forma[i])):
                if self.forma[i][j] == "X" and tablero[(self.y//tamano_bloque)+i][(self.x//tamano_bloque)+j] == "X":
                    pygame.draw.rect(pantalla, self.color, (self.x + j * tamano_bloque, self.y + i * tamano_bloque, tamano_bloque, tamano_bloque))
                    pygame.draw.rect(pantalla, NEGRO, (self.x + j * tamano_bloque, self.y + i * tamano_bloque, tamano_bloque, tamano_bloque), 1)
    
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
tablero = [["." for _ in range(ancho_pantalla // tamano_bloque)] for _ in range(alto_pantalla // tamano_bloque)]

# Variables para controlar el juego
pieza_actual = nueva_pieza()
tiempo_pieza = 0
tiempo_total = 0
puntaje = 0
tiempo = 1000
game_over = False
anterior_piezas = []

# Bucle principal del juego
while not game_over:
    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            game_over = True
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                pieza_actual.mover_izquierda()
                if pieza_actual.colision(tablero):
                    pieza_actual.mover_derecha()
            elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                pieza_actual.mover_derecha()
                if pieza_actual.colision(tablero):
                    pieza_actual.mover_izquierda()
            elif evento.key == pygame.K_UP or evento.key == pygame.K_w:
                pieza_actual.girar()
                if pieza_actual.colision(tablero):
                    pieza_actual.girar()
            elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                pieza_actual.mover_abajo()
                if pieza_actual.colision(tablero):
                    pieza_actual.mover_arriba()
    # Actualización del juego
    tiempo_pieza += reloj.tick(60)
    tiempo_total += tiempo_pieza
    if tiempo_pieza > tiempo:
        pieza_actual.mover_abajo()
        if pieza_actual.colision(tablero):
            pieza_actual.mover_arriba()
            if pieza_actual.y <= 0:
                game_over = True
            for i in range(len(pieza_actual.forma)):
                for j in range(len(pieza_actual.forma[i])):
                    if pieza_actual.forma[i][j] == "X":
                        if 0 <= ((pieza_actual.y + i)//tamano_bloque) < len(tablero) and 0 <= ((pieza_actual.x + j)//tamano_bloque) < len(tablero[0]):
                            tablero[(pieza_actual.y)//tamano_bloque+i][(pieza_actual.x//tamano_bloque)+j] = "X"
            filas_completas = 0
            for i in range(len(tablero)):
                if "." not in tablero[i]:
                    filas_completas += 1
                    del tablero[i]
                    tablero.insert(0, ["." for _ in range(ancho_pantalla // tamano_bloque)])
                    puntaje += filas_completas*100
                    print(f" Score: {puntaje}")
                    tiempo -= 50
                    if tiempo < 300:
                        tiempo = 200
            anterior_piezas.append(PiezaVieja(pieza_actual.forma,pieza_actual.color,pieza_actual.x,pieza_actual.y))
            pieza_actual = nueva_pieza()
        tiempo_pieza = 0

    # Dibujar la pantalla del juego
    pantalla.fill(GRIS)
    pieza_actual.dibujar()
    if anterior_piezas != []:
        for i in anterior_piezas:
            i.dibujar()
    pygame.display.flip()

print("¡Juego terminado!")
print("Puntaje final:", puntaje,"\n")
file = open('scoreboard.csv', 'a') # Open the file in append mode
file.write("\n")
file.write(str(puntaje))
file.close()

rows = []
file = open("scoreboard.csv","r+")
csvreader = csv.reader(file)
header = next(csvreader)
for row in csvreader:
    rows.append(row)
scoreboard = []
for i in rows:
    scoreboard.append(int(i[0]))

if max(scoreboard) <= puntaje:
    print(f"New record! {puntaje}")
print(f"Highscore: {max(scoreboard)}")

pygame.quit()
