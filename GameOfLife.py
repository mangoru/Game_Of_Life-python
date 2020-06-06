import pygame
import numpy as np
import time 

pygame.init()
#creamos pantalla screen    
width, heigth = 700 , 700
screen = pygame.display.set_mode((width, heigth))

#elegimos color de fondo1
bg = 25, 25, 25
grey = 128, 128, 128
white = 255, 255, 255
screen.fill(bg)

#dimenciones de las celdas
nxC, nyC = 50,50
dimCW = width/nxC
dimCH = heigth/nyC

#matriz de estados de celda, muerta=9 viva=1
gameState = np.zeros((nxC,nyC)) #crea matriz llena de ceros

pauseRun = False

running = True

while running:

    newgameState = np.copy(gameState)
#entos del teoclado o mouse
    ev = pygame.event.get()

    for event in ev:

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                newgameState = np.zeros((nxC,nyC))
            else:
                pauseRun = not(pauseRun) 

        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            x, y = int(np.floor(posX/dimCW)), int(np.floor(posY/dimCH))
            #newStatus[x,y] = np.abs(newStatus[x,y]-1)
            newgameState[x,y] = not mouseClick[2]
# if event.type == pygame.KEYDOWN:
    
    screen.fill(bg)

    for y in range(0,nyC):
        for x in range(0,nxC):
            
            if not pauseRun:
                #contamos el numero de vecinos cercanos
                n_neigh =   gameState[(x-1)%nxC,(y-1)%nyC] + \
                            gameState[(x)%nxC  ,(y-1)%nyC] + \
                            gameState[(x+1)%nxC,(y-1)%nyC] + \
                            gameState[(x-1)%nxC,(y)%nyC] + \
                            gameState[(x+1)%nxC,(y)%nyC] + \
                            gameState[(x-1)%nxC,(y+1)%nyC] + \
                            gameState[(x)%nxC  ,(y+1)%nyC] + \
                            gameState[(x+1)%nxC,(y+1)%nyC] 
                
                #rule1: una celuca muerta con exactamente 3 vecinas vivas , revive
                if gameState[x,y] == 0 and n_neigh == 3:
                    newgameState[x,y] = 1
                #rule2: una celula viva con menos de 2 o mas de 3 vecinas vivas, muere
                elif gameState[x,y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newgameState[x,y] = 0

            #literalmente dibujamos celda por celda 
            poly = [((x) * dimCW,  y *  dimCH),
                    ((x+1)*dimCW,  y *  dimCH),
                    ((x+1)*dimCW, (y+1)*dimCH),
                    ((x) * dimCW ,(y+1)*dimCH)
                    ]

            if newgameState[x,y] == 1:
                pygame.draw.polygon(screen,white,poly,0)
            else:
                pygame.draw.polygon(screen,grey,poly,1)
    #actualizacion de pantalla
    gameState = np.copy(newgameState)
    time.sleep(0.1)
    pygame.display.flip()

pygame.quit()
