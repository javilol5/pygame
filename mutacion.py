import pygame
import random
import time

# --- Configuración ---
ANCHO = 40
ALTO = 90
TAM_CELDA = 10
MARGEN = 2

VENTANA_ANCHO = ANCHO * TAM_CELDA
VENTANA_ALTO = ALTO * TAM_CELDA

COLORES = [
    (255, 0, 0),    # rojo
    (0, 255, 0),    # lima
    (0, 0, 255),    # azul
    (255, 255, 0),  # amarillo
    (255, 0, 255),  # magenta
    (0, 255, 255),  # cyan
    (255,255,255),  # blanco
    (0,0,0),        # negro
    (179,179,179),  # gris
    (153,0,204),    # morado
    (255,102,0),    # naranja
    (255,153,204),  # rosa
    (102,51,51),    # marron
    (0,102,51),     # verde
    (233,69,67),    # adrian
    (177,124,232)   # gabriela
    ]

# --- Inicialización ---
pygame.init()
pantalla = pygame.display.set_mode((VENTANA_ANCHO, VENTANA_ALTO))
pygame.display.set_caption("Juego de Mutación Vecinal")
reloj = pygame.time.Clock()

# --- Crear cuadrícula ---
grid = []
for y in range(ALTO):
    fila = []
    for x in range(ANCHO):
        fila.append({
            #"color": random.choice(COLORES),
            "color": (0, 0, 0),  # iniciar todo en rojo para ver mutaciones
            "visible": True,
            "reaparicion": None
        })
    grid.append(fila)

# --- Funciones ---
def vecinos_visibles(x, y):
    vecinos = []
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < ANCHO and 0 <= ny < ALTO:
            celda = grid[ny][nx]
            if celda["visible"]:
                vecinos.append(celda["color"])
    return vecinos

def mutar_color(color_actual):
    opciones = [c for c in COLORES if c != color_actual]
    return random.choice(opciones)

def tocar_celda(x, y, tiempo_actual):
    celda = grid[y][x]
    if celda["visible"]:
        celda["visible"] = False
        celda["color"] = None  # olvida su color
        celda["reaparicion"] = tiempo_actual + 2

# --- Variables para arrastrar ---
raton_pulsado = False
ultima_celda = None

# --- Bucle principal ---
ejecutando = True
while ejecutando:
    reloj.tick(60)
    tiempo_actual = time.time()

    # --- Eventos ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                raton_pulsado = True

        if evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1:
                raton_pulsado = False
                ultima_celda = None  # reiniciar al soltar

    # --- Arrastrar / Clic continuo ---
    if raton_pulsado:
        mx, my = pygame.mouse.get_pos()
        x = mx // TAM_CELDA
        y = my // TAM_CELDA

        if 0 <= x < ANCHO and 0 <= y < ALTO:
            if ultima_celda != (x, y):
                tocar_celda(x, y, tiempo_actual)
                ultima_celda = (x, y)

    # --- Reapariciones ---
    for y in range(ALTO):
        for x in range(ANCHO):
            celda = grid[y][x]
            if not celda["visible"] and celda["reaparicion"] <= tiempo_actual:
                vecinos = vecinos_visibles(x, y)
                if vecinos:
                    # Hay vecinos visibles
                    nuevo_color = random.choice(vecinos)
                    # Probabilidad de mutar
                    if random.random() < 0.05:
                        nuevo_color = mutar_color(nuevo_color)
                    celda["color"] = nuevo_color
                    celda["visible"] = True
                    celda["reaparicion"] = None
                else:
                    # No hay vecinos visibles: espera a que aparezcan
                    celda["reaparicion"] = tiempo_actual + 0.5  # revisa cada medio segundo

    # --- Dibujar ---
    pantalla.fill((30, 30, 30))
    for y in range(ALTO):
        for x in range(ANCHO):
            celda = grid[y][x]
            if celda["visible"]:
                pygame.draw.rect(
                    pantalla,
                    celda["color"],
                    (
                        x * TAM_CELDA + MARGEN,
                        y * TAM_CELDA + MARGEN,
                        TAM_CELDA - MARGEN * 2,
                        TAM_CELDA - MARGEN * 2
                    )
                )

    pygame.display.flip()

pygame.quit()
