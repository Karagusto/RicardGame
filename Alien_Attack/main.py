import pygame

pygame.init()

# definitions of colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

lead_x_change = 0
lead_y_change = 0

screenWidth = 500
screenHeight = 500

x = 250
y = 250
width = 20
height = 20
vel = 15

isJump = False
jumpCount = 10
left = False
right = False
walkCount = 0

win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('Game/R1.png'), pygame.image.load('Game/R2.png'), pygame.image.load('Game/R3.png'), pygame.image.load('Game/R4.png'), pygame.image.load('Game/R5.png'), pygame.image.load('Game/R6.png'), pygame.image.load('Game/R7.png'), pygame.image.load('Game/R8.png'), pygame.image.load('Game/R9.png')]
walkLeft = [pygame.image.load('Game/L1.png'), pygame.image.load('Game/L2.png'), pygame.image.load('Game/L3.png'), pygame.image.load('Game/L4.png'), pygame.image.load('Game/L5.png'), pygame.image.load('Game/L6.png'), pygame.image.load('Game/L7.png'), pygame.image.load('Game/L8.png'), pygame.image.load('Game/L9.png')]
bg = pygame.image.load('Game/bg.jpg')
char = pygame.image.load('Game/standing.png')



run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_q]:
        run = False
    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
    if keys[pygame.K_RIGHT] and x < screenWidth - width - vel:
        x += vel
    if not (isJump):
        # if keys[pygame.K_UP] and y > vel:
        #     y -= vel
        # if keys[pygame.K_DOWN] and y < screenWidth - height - vel:
        #     y += vel
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= (jumpCount ** 2) * 0.5 * neg
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10


    # if keys[pygame.K_q]:
    #     run = False
    # if keys[pygame.K_LEFT] and x > vel:
    #     lead_x_change -= vel
    # if keys[pygame.K_RIGHT] and x < screenWidth - width - vel:
    #     lead_x_change += vel
    # if keys[pygame.K_UP] and y > vel:
    #     lead_y_change -= vel
    # if keys[pygame.K_DOWN] and y < screenWidth - height - vel:
    #     lead_y_change += vel

    # x += lead_x_change
    # y += lead_y_change

    win.fill(black)
    pygame.draw.rect(win, red, (x, y, width, height))
    pygame.display.update()



pygame.quit()