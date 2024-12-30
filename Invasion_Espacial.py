import pygame
import random
import math
from pygame import mixer
import io

# Iniciar Pygame
pygame.init()

# Crear la pantalla del juego
pantalla = pygame.display.set_mode((800,600))

# Titulo, Fondo e Icono
pygame.display.set_caption("Invasión Espacial")

icono = pygame.image.load("cohete.png")
pygame.display.set_icon(icono)

fondo = pygame.image.load("galaxy.jpg")

# Agregar musica
mixer.music.load("MusicaFondo.mp3")
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# Variables del jugador
img_nave = pygame.image.load("astronave.png")
nave_x_cambio = 0
enemigos = 8

# Variables de los enemigos
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_de_enemigos = 8

for e in range(cantidad_de_enemigos):
    img_enemigo.append(pygame.image.load("ovni.png"))
    enemigo_x.append(random.randint(0,736))
    enemigo_y.append(random.randint(50,200))

    enemigo_x_cambio.append(0.4)
    enemigo_y_cambio.append(50)

# Variables de la bala
img_bala = pygame.image.load("bala.png")
bala_x = 0
bala_y = 500 #Posicion inicial encima del cohete
bala_x_cambio = 0
bala_y_cambio = 1 #Velocidad bala
bala_visible = False
balas = []

# Puntaje
puntaje = 0

fuente = pygame.font.Font("QuirkyRobot.ttf",32)
texto_x = 10
texto_y = 10

# Configuracion texto final de juego
fuente_final = pygame.font.Font("QuirkyRobot.ttf",60)

# Configuracion de texto si ganaste
fuente_ganaste = pygame.font.Font("QuirkyRobot.ttf",60)

# Funcion mostrar texto si pierdes
def texto_final():
    mi_fuente_final = fuente_final.render("GAME OVER",True,(255,255,255))
    pantalla.blit(mi_fuente_final,(280,200))

# Funcion mostrar texto si ganas
def texto_ganaste():
    mi_fuente_ganaste = fuente_ganaste.render("FELICITACIONES GANASTE!",True,(255,255,255))
    pantalla.blit(mi_fuente_ganaste,(130,240))

# Funcion mostrar puntaje
def mostrar_puntaje(x,y):
    texto = fuente.render(f"Puntaje: {puntaje}",True,(255,255,255))
    pantalla.blit(texto,(x,y))

# Funcion jugador
def nave(x,y):
    pantalla.blit(img_nave,(x,y))

# Funcion enemigo
def enemigo(x,y,ene):
    pantalla.blit(img_enemigo[ene],(x,y))

# Funcion disparar bala
def dispara_bala(x,y):
    global bala_visible
    bala_visible = True

    pantalla.blit(img_bala,(x+16,y+10))

# Funcion detectar colision
def hay_colision(x_1,y_1,x_2,y_2):
    distancia = math.sqrt(math.pow(x_2-x_1,2) + math.pow(y_2-y_1,2))
    if distancia < 27:
        return True
    else:
        return False

# Loop del juego
se_ejecuta = True

while se_ejecuta:

    # Imagen de fondo
    pantalla.blit(fondo,(0,0))

    # Mostrar Puntaje
    mostrar_puntaje(texto_x,texto_y)

    # Posicionar la nave solo en Eje X segun la posicion del mouse
    mouse_pos = pygame.mouse.get_pos()
    nave_x = mouse_pos[0] #Valor 0 para eje X y valor 1 para eje Y
    nave_y = 500

    # Revision de cada evento
    for evento in pygame.event.get():

        # Evento presionar x para cerrar programa
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                se_ejecuta = False

        # Evento presionar boton izquierdo del mouse
        if evento.type == pygame.MOUSEBUTTONDOWN:
            sonido_bala = mixer.Sound("disparo.mp3")
            sonido_bala.set_volume(0.3)
            sonido_bala.play()
            nueva_bala = {"x": nave_x,"y": nave_y,"velocidad": -3}
            balas.append(nueva_bala)

    # Mantener dentro de pantalla jugador
    if nave_x <= 0:
        nave_x = 0
    elif nave_x >= 734:
        nave_x = 734

    # Mover enemigo
    for e in range(cantidad_de_enemigos):

        # Verificar si has ganado
        if puntaje >= 10:
            for k in range(cantidad_de_enemigos):
                enemigo_y[k] = 1000
            texto_ganaste()
            break

        # Fin del juego
        if enemigo_y[e] >= 470:
            for k in range(cantidad_de_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

        # Mantener dentro de pantalla enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.4
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 734:
            enemigo_x_cambio[e] = -0.4
            enemigo_y[e] += enemigo_y_cambio[e]

        # Verificar colision
        for bala in balas:
            colision_bala_enemigo = hay_colision(enemigo_x[e],enemigo_y[e],bala["x"],bala["y"])

            if colision_bala_enemigo:
                sonido_colision = mixer.Sound("golpe.mp3")
                sonido_colision.play()
                balas.remove(bala)
                puntaje += 1
                enemigos -= 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(50, 200)

        enemigo(enemigo_x[e], enemigo_y[e],e)

    # Movimiento bala
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala,(bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)

    if bala_visible:
        dispara_bala(bala_x,bala_y)
        bala_y -= bala_y_cambio

    nave(nave_x,nave_y)

    # Actualizar
    pygame.display.update()



