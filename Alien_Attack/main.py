import pygame
import random

pygame.init()


class background(object):
    def __init__(self, screenwidth, screenheight):
        self.screenwidth = screenwidth
        self. screenheight = screenheight

    def drawBackground(self):
        win = pygame.display.set_mode((500, 480))
        pygame.display.set_caption("First Game")
        return win


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 15, self.y + 10, self.width//2, self.height)

    def draw(self, win):
        if self.walkCount + 1 >= 1:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            win.blit(char, (self.x, self.y))
        self.hitbox = (self.x + 15, self.y + 10, self.width//2, self.height)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        print("hit")
        pass

class projectile(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        # self.facing = facing
        self.vel = 8
        self.hitbox = (self.x - 20, self.y - 20, 20, 20)

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        self.hitbox = (self.x - 10, self.y - 10, 20, 20)
        pygame.draw.rect(win, self.color, self.hitbox, 2)

class enemy(object):
    enemySprite = [pygame.image.load('Game/invader.gif')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.y, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x, self.y, self.width//2, self.height//2)

    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= 1:
            self.walkCount = 0
        if self.vel > 0:
            win.blit(self.enemySprite[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.enemySprite[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        self.hitbox = (self.x, self.y, self.width//2 - 10, self.height//2 - 10)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        pass

    def move(self):
        if self.vel > 0:
            if self.y + self.vel < self.path[1]:
                self.y += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.y - self.vel > self.path[0]:
                self.y += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        pass

    def hit(self):
        print("hit")
        pass


#Class for collision development
class collision(object):

    def __init__(self, hitbox1, hitbox2):
        self.hitbox1 = hitbox1
        self.hitbox2 = hitbox2

    def isCollidingEnemy(self, hitbox1, hitbox2):
        if hitbox1[1] - hitbox1[3] < hitbox2[1] + hitbox2[3] and hitbox1[1] + hitbox1[3] > hitbox2[1]:
            if hitbox1[0] + hitbox1[2] > hitbox2[0] and hitbox1[0] - hitbox1[2]  < hitbox2[0] + hitbox2[2]:
                print("HIT")

    # def isCollidingBullet(self, hitbox, ):



bgnd = background(500, 480)
win = bgnd.drawBackground()
man = player(200, 410, 64, 64)
goblin = enemy(200, 0, 64, 64, 480)
# bullet = projectile(round(man.x + man.width/2), man.y, 3, (255, 0, 0))


walkRight = [pygame.image.load('Game/R1.png'), pygame.image.load('Game/R2.png'), pygame.image.load('Game/R3.png'), pygame.image.load('Game/R4.png'), pygame.image.load('Game/R5.png'), pygame.image.load('Game/R6.png'), pygame.image.load('Game/R7.png'), pygame.image.load('Game/R8.png'), pygame.image.load('Game/R9.png')]
walkLeft = [pygame.image.load('Game/L1.png'), pygame.image.load('Game/L2.png'), pygame.image.load('Game/L3.png'), pygame.image.load('Game/L4.png'), pygame.image.load('Game/L5.png'), pygame.image.load('Game/L6.png'), pygame.image.load('Game/L7.png'), pygame.image.load('Game/L8.png'), pygame.image.load('Game/L9.png')]
bg = pygame.image.load('Game/bg.jpg')
char = pygame.image.load('Game/standing.png')
#
# walkRight = [pygame.image.load('Game/ally.gif')]
# walkLeft = [pygame.image.load('Game/ally.gif')]
# char = pygame.image.load('Game/ally.gif')
# bg = pygame.image.load('Game/space_invaders_background.gif')

clock = pygame.time.Clock()
bullets = []
enemies = []

def redrawGameWindow():
    win.blit(bg, (0, 0))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()



run = True
while run:
    clock.tick(27)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_q]:
            run = False
    for bullet in bullets:

        if bullet.y < 500 and bullet.y > 0:
            bullet.y -= bullet.vel
        else:
            bullets.pop(bullets.index(bullet))



    if keys[pygame.K_SPACE]:
        if len(bullets) < 1:
            bullets.append(projectile(round(man.x + man.width//2), round(man.y + man.height//2), 6, (0, 0, 0)))

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if not (man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()

pygame.quit()