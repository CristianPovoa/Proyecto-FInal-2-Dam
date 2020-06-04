import pygame
import time
import random
import sqlite3
#Anular mensaje DeprecationWarning
import sys
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")    

#Inciamos pygame
pygame.init()
pygame.mixer.music.load("C:/Users/Usuario/Desktop/Proyecto_Final_Serpiente/serpiente.mp3")
pygame.mixer.music.play()

#Declaración de constantes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED= (255, 0, 0)
BLUE = (99, 166, 247)
BLUE2 = (73, 242, 189)
GOLD = (235, 158, 52)
VIOLET = (161, 79, 255)
AZULTUR= (23, 207, 133)


#Creación de la ventana
display_ancho = 700
display_altura = 500
superficie = pygame.display.set_mode((display_ancho,display_altura))
pygame.display.set_caption("Jörmundgander")


#Creacion de variables
reloj = pygame.time.Clock()
fondo = pygame.image.load('C:/Users/Usuario/Desktop/Proyecto_Final_Serpiente/fondoinicio1.jpg').convert_alpha()
fondojuego = pygame.image.load('C:/Users/Usuario/Desktop/Proyecto_Final_Serpiente/cesped.jpg').convert_alpha()
fondogameover = pygame.image.load('C:/Users/Usuario/Desktop/Proyecto_Final_Serpiente/gameover1.jpg').convert_alpha()
f_pausa = pygame.image.load('C:/Users/Usuario/Desktop/Proyecto_Final_Serpiente/fondopausa.jpg').convert_alpha()
bloque_tamano = 10
FPS = 20
font = pygame.font.SysFont(None, 25)

#Funciones
def intro_juego():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    
        superficie.fill(GOLD)
        superficie.blit(fondo, [0, 0])  #Una imagen que queramos
        message_to_screen("Bienvenid@ a Jörmundgander", GOLD, -100)
        message_to_screen("El objetivo del juego es comerse todas las manzanas,", BLUE2, -50)
        message_to_screen("Mientras más manzanas comas, mas grande se hara la serpiente.", BLUE2, -30)
        message_to_screen("No te choques con las paredes ni te comas a ti mismo, o perderas", BLUE2, -10)
        message_to_screen("Para jugar pulse C. Para salir pulse Q", BLUE2, 100)

        pygame.display.update()
        reloj.tick(15)

def puntos (puntuacion):
    text = font.render("Puntos: " + str(puntuacion), True, GOLD)
    superficie.blit(text, [0, 0])

def pausa():
    pausado = True
    while pausado:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if  event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    pausado = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        superficie.fill(BLUE)
        superficie.blit(f_pausa, [0, 0]) 
        message_to_screen("Pausa", RED, -100)
        message_to_screen("Hay que descansar de vez en cuando", BLUE2, -75)
        message_to_screen("Para volver a jugar, pulse C. Para terminar, pulse Q", BLUE2, 25)
        pygame.display.update()
        reloj.tick(5)
       
def serpiente(bloque_tamano, listaSerp):
    for XandY in listaSerp:
        pygame.draw.rect(superficie, BLACK, [XandY[0], XandY[1], bloque_tamano, bloque_tamano])  

def text_objetos(text, color):
    textSuperficie = font.render(text, True, color)
    return textSuperficie, textSuperficie.get_rect()

def message_to_screen(msg, color, y_displace = 0, tamano_letra = "pequeña"):
    textSur, textRect = text_objetos(msg, color)
    textRect.center = (display_ancho/2), (display_altura/2) + y_displace
    superficie.blit(textSur, textRect)
    
def gameLoop():
    gameExit = False
    gameOver = False
    
    #Cabeza de la serpiente
    lead_x = display_ancho/2
    lead_y = display_altura/2
    
    lead_x_cambio = 0
    lead_y_cambio = 0
    
    listaSerp = []
    largoSerp = 1
    
    #Lugar y tamaño de la manzana
    azarManzana_x = round(random.randrange(0, display_ancho - bloque_tamano)/10.0)*10.0
    azarManzana_y = round(random.randrange(0, display_altura - bloque_tamano)/10.0)*10.0
    
    while not gameExit:
        while gameOver == True:
            superficie.fill(VIOLET)
            superficie.blit(fondogameover, [0, 0])  #Una imagen que queramos
            message_to_screen("Para volver a jugar, pulse C. Para terminar, pulse Q", BLACK, -100)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame. KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()
        #Movimiento de la Serpiente 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_cambio = -bloque_tamano
                    lead_y_cambio = 0
                elif event.key == pygame.K_RIGHT:
                    lead_x_cambio = +bloque_tamano
                    lead_y_cambio = 0
                elif event.key == pygame.K_UP:
                    lead_y_cambio = -bloque_tamano
                    lead_x_cambio = 0
                elif event.key == pygame.K_DOWN:
                    lead_y_cambio = +bloque_tamano
                    lead_x_cambio = 0
                elif event.key == pygame.K_p:
                    pausa()
        #Cierre del juego si la serpiente toca uno de los bordes        
        if lead_x >= display_ancho or lead_x < 0 or lead_y >= display_altura or lead_y < 0:
            gameOver = True
            
        lead_x += lead_x_cambio
        lead_y += lead_y_cambio 
       
        superficie.blit(fondojuego, [0, 0])  #Una imagen que queramos
        tamanoManza = 25
        pygame.draw.rect(superficie, RED, [azarManzana_x, azarManzana_y, tamanoManza, tamanoManza])
        
        cabezaSerp = []
        
        #añadimos una cabeza más cuando coma la manzana
        cabezaSerp.append(lead_x)
        cabezaSerp.append(lead_y)
        listaSerp.append(cabezaSerp)
        if len(listaSerp) > largoSerp:
            del listaSerp[0]
        
        for eachSegment in listaSerp[:-1]:
            if eachSegment == cabezaSerp:
                gameOver = True
            
        serpiente(bloque_tamano, listaSerp)
        puntos(largoSerp -1)
        pygame.display.update()
        
        #Hacemos que se genere en un nuevo sitio al azar cuando pasamos sobre ella.
        if lead_x >= azarManzana_x and lead_x <= azarManzana_x + tamanoManza:
            if lead_y >= azarManzana_y and lead_y <= azarManzana_y + tamanoManza:
                azarManzana_x = round(random.randrange(0, display_ancho - bloque_tamano)/10.0)*10.0
                azarManzana_y = round(random.randrange(0, display_altura - bloque_tamano)/10.0)*10.0
                largoSerp += 1 #Agrega un bloque más a la serpiente
               
        reloj.tick(FPS)
        
    pygame.quit()
    quit()
    
intro_juego()
gameLoop()