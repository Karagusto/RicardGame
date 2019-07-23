import pygame

pygame.init()


white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Alien Attack')

gameExit = False

while not gameExit:
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            gameExit = True

    gameDisplay.fill(white)
    pygame.draw.rect(gameDisplay, black, [400, 300, 10, 100])
    pygame.draw.rect(gameDisplay, red, [400, 300, 10, 10])

    gameDisplay.fill(red, rect=[200,200, 50, 50])

    pygame.display.update()


pygame.quit()
quit()
