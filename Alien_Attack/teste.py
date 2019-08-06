import pygame
import random

pygame.init()


class background(object):
    def __init__(self, screenwidth, screenheight):
        self.screenwidth = screenwidth
        self. screenheight = screenheight

    def drawBackground(self):
        win = pygame.display.set_mode((self.screenwidth, self.screenheight))
        pygame.display.set_caption("Space Invaders")
        return win

    # def drawStartScreen(self):



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
        self.health = 10
        self.visible = True

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
        self.hitbox = (self.x + 5, self.y, self.width//2 - 7, self.height//2)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
        pygame.draw.rect(win, (0, 255, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - ((50/10) * (10 - self.health)), 10))
    def hit(self):
        if self.health > 0:
            self.health -= 1
            return self.health
        else:
            self.visible = False
            return self.health
        print("hit")

    def score(self):
        return 10

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
        #pygame.draw.rect(win, self.color, self.hitbox, 2)

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
        self.health = 1
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 1:
                self.walkCount = 0
            if self.vel > 0:
                win.blit(self.enemySprite[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.enemySprite[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            self.hitbox = (self.x, self.y, self.width//2 - 3, self.height//2 - 3)
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
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
        print("boom!")
        self.visible = False
        pass


#Class for collision development
class collision(object):

    def __init__(self, hitbox1, hitbox2, hitbox, projectile):
        self.hitbox1 = hitbox1
        self.hitbox2 = hitbox2
        self.hitbox = hitbox
        self.projectile = projectile

    def isCollidingEnemy(self, hitbox1, hitbox2):
        if self.hitbox1[0] >= self.hitbox2[0] and self.hitbox1[0] < self.hitbox2[0] + self.hitbox2[2] or self.hitbox1[0] + self.hitbox1[2] >= self.hitbox2[0] and self.hitbox1[0] + self.hitbox1[2] < self.hitbox2[0] + self.hitbox2[2]:
            #print("xcrossover")
            if self.hitbox1[1] >= self.hitbox2[1] and self.hitbox1[1] < self.hitbox2[1] + self.hitbox2[3] or self.hitbox1[1] + self.hitbox1[3] >= self.hitbox2[1] and self.hitbox1[1] + self.hitbox1[3] < self.hitbox2[1] + self.hitbox2[3]:
                #print("xandycrossover")
                return 0

    def isCollidingBullet(self):
        if self.hitbox[1] - self.hitbox[3] < self.projectile.y + self.projectile.radius and self.hitbox[1] + self.hitbox[3] > self.projectile.y:
            if self.hitbox[0] + self.hitbox[2] > self.projectile.x and self.hitbox[0] - self.hitbox[2] < self.projectile.x + self.projectile.radius:
                return 0
    #
    # if lead_x > randAppleX and lead_x < randAppleX + AppleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + AppleThickness:
    #     # print("x crossover")
    #     if lead_y > randAppleY and lead_y < randAppleY + AppleThickness or lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness:




# bullet = projectile(round(man.x + man.width/2), man.y, 3, (255, 0, 0))


# walkRight = [pygame.image.load('Game/R1.png'), pygame.image.load('Game/R2.png'), pygame.image.load('Game/R3.png'), pygame.image.load('Game/R4.png'), pygame.image.load('Game/R5.png'), pygame.image.load('Game/R6.png'), pygame.image.load('Game/R7.png'), pygame.image.load('Game/R8.png'), pygame.image.load('Game/R9.png')]
# walkLeft = [pygame.image.load('Game/L1.png'), pygame.image.load('Game/L2.png'), pygame.image.load('Game/L3.png'), pygame.image.load('Game/L4.png'), pygame.image.load('Game/L5.png'), pygame.image.load('Game/L6.png'), pygame.image.load('Game/L7.png'), pygame.image.load('Game/L8.png'), pygame.image.load('Game/L9.png')]
# bg = pygame.image.load('Game/bg.jpg')
# char = pygame.image.load('Game/standing.png')
#
walkRight = [pygame.image.load('Game/ally.gif')]
walkLeft = [pygame.image.load('Game/ally.gif')]
char = pygame.image.load('Game/ally.gif')
bg = pygame.image.load('Game/space_invaders_background.gif')
font = pygame.font.SysFont(None, 25)
clock = pygame.time.Clock()


# object for texts
def text_objects(text, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


# display message to screen
def message_to_screen(msg, color, bgnd, win):
    textSurface, textRect = text_objects(msg, color)

    # screen_text = font.render(msg, True, color)
    # gameDisplay.blit(screen_text, [display_width / 2, display_height / 2])
    textRect.center = (bgnd.screenwidth/2), (bgnd.screenheight/2)
    win.blit(textSurface, textRect)


def redrawGameWindow(win, man, goblin, bullets, score, isdead):
    win.blit(bg, (0, 0))
    text = font.render('Score: ' + str(score), 1, (255, 255, 255))
    win.blit(text, (390, 10))
    man.draw(win)
    goblin.draw(win)

    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


#goblin = enemy(random.randrange(70, 420), 0, 64, 64, 480)
def game_loop():

    gameExit = False
    gameOver = False
    isdead = True
    shootLoop = 0
    score = 0
    bullets = []
    enemies = []

    bgnd = background(500, 480)
    win = bgnd.drawBackground()
    man = player(200, 410, 64, 64)
    goblin = 0






    while not gameExit:
        if isdead == True:
            new_goblin = enemy(random.randrange(70, 420), 0, 64, 64, 480)
            goblin = new_goblin
            isdead = False

        keys = pygame.key.get_pressed()
        #message_to_screen("Score: ", (255, 255, 255), bgnd, win)
        pygame.display.update()
        while gameOver == True:
            win.fill((255, 255, 255))
            message_to_screen("Game Over, press C to play again or Q to quit", (255, 0, 0), bgnd, win)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        game_loop()
        if shootLoop > 0:
            shootLoop += 1
        if shootLoop > 3:
            shootLoop = 0



        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT or keys[pygame.K_q]:
                gameExit = True
        for i in range(1,2):
            aliens = enemy(random.randrange(70, 420), 0, 64, 64, 480)
            enemies.append(aliens)
        for bullet in bullets:
            col = collision(0, 0, goblin.hitbox, bullet)

            if bullet.y < 500 and bullet.y > 0:
                bullet.y -= bullet.vel
                if collision.isCollidingBullet(col) == 0:
                    bullets.pop(bullets.index(bullet))
                    alien.hit()
                    isdead = True
                    score += man.score()
            else:
                bullets.pop(bullets.index(bullet))

        # for alien in enemies:
        alien = goblin
        col2 = collision(alien.hitbox, man.hitbox, 0, 0)
        if collision.isCollidingEnemy(col2, man.hitbox, alien.hitbox) == 0:
            health = man.hit()
            if health > 0:
                print("zpiurr!")
            else:
                gameOver = True




        if keys[pygame.K_SPACE] and shootLoop == 0:
            if len(bullets) < 5:
                bullets.append(projectile(round(man.x + man.width//2), round(man.y + man.height//2), 6, (255, 255, 255)))

            shootLoop = 1

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

        clock.tick(27)
        redrawGameWindow(win, man, goblin, bullets, score, isdead)

    # while run:
    #     clock.tick(27)
    #     keys = pygame.key.get_pressed()
    #
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT or keys[pygame.K_q]:
    #             run = False
    #     while gameOver == True:
    #         win.fill((255, 255, 255))
    #         message_to_screen("Game Over, press C to play again or Q to quit", (255, 0, 0))
    #         pygame.display.update()
    #         for event2 in pygame.event.get():
    #             if event2.type == pygame.QUIT or keys[pygame.K_q]:
    #                 run = False
    #                 gameOver = False
    #             if event2.type == keys[pygame.K_c]:
    #                 gameOver = False
    #                 game_loop()
    #     for bullet in bullets:
    #         col = collision(0, 0, goblin.hitbox, bullet)
    #
    #         if bullet.y < 500 and bullet.y > 0:
    #             bullet.y -= bullet.vel
    #             if collision.isCollidingBullet(col) == 0:
    #                 bullets.pop(bullets.index(bullet))
    #         else:
    #             bullets.pop(bullets.index(bullet))
    #
    #     # for alien in enemies:
    #     alien = goblin
    #     col2 = collision(alien.hitbox, man.hitbox, 0, 0)
    #     if collision.isCollidingEnemy(col2, man.hitbox, alien.hitbox) == 0:
    #         print("Hit")
    #         gameOver = True
    #
    #
    #
    #
    #     if keys[pygame.K_SPACE]:
    #         if len(bullets) < 1:
    #             bullets.append(projectile(round(man.x + man.width//2), round(man.y + man.height//2), 6, (0, 0, 0)))
    #
    #     if keys[pygame.K_LEFT] and man.x > man.vel:
    #         man.x -= man.vel
    #         man.left = True
    #         man.right = False
    #         man.standing = False
    #     elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
    #         man.x += man.vel
    #         man.right = True
    #         man.left = False
    #         man.standing = False
    #     else:
    #         man.standing = True
    #         man.walkCount = 0
    #
    #     if not (man.isJump):
    #         if keys[pygame.K_UP]:
    #             man.isJump = True
    #             man.right = False
    #             man.left = False
    #             man.walkCount = 0
    #     else:
    #         if man.jumpCount >= -10:
    #             neg = 1
    #             if man.jumpCount < 0:
    #                 neg = -1
    #             man.y -= (man.jumpCount ** 2) * 0.5 * neg
    #             man.jumpCount -= 1
    #         else:
    #             man.isJump = False
    #             man.jumpCount = 10
    #
    #     redrawGameWindow()

    pygame.quit()
    quit()

game_loop()
# import pygame
# import numpy as np
# import random
#
# pygame.init()
#
#
# class background(object):
#     def __init__(self, screenwidth, screenheight):
#         self.screenwidth = screenwidth
#         self. screenheight = screenheight
#
#     def drawBackground(self):
#         win = pygame.display.set_mode((500, 480))
#         pygame.display.set_caption("Alien Attack 0.0.1")
#         return win
#
#
# class player(object):
#     def __init__(self, x, y, width, height):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.vel = 5
#         self.isJump = False
#         self.left = False
#         self.right = False
#         self.walkCount = 0
#         self.jumpCount = 10
#         self.standing = True
#
#     def draw(self, win):
#         if self.walkCount + 1 >= 1:
#             self.walkCount = 0
#
#         if not(self.standing):
#             if self.left:
#                 win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
#                 self.walkCount += 1
#             elif self.right:
#                 win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
#                 self.walkCount += 1
#         else:
#             win.blit(char, (self.x, self.y))
#
#
# class projectile(object):
#     def __init__(self, x, y, radius, color):
#         self.x = x
#         self.y = y
#         self.radius = radius
#         self.color = color
#         # self.facing = facing
#         self.vel = 8
#
#     def draw(self, win):
#         pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
#
# class enemy(object):
#     enemySprite = [pygame.image.load('Game/invader.gif')]
#
#     def __init__(self, x, y, width, height, end):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.end = end
#         self.path = [self.y, self.end]
#         self.walkCount = 0
#         self.vel = 3
#
#     def draw(self, win):
#         self.move()
#         if self.walkCount + 1 >= 1:
#             self.walkCount = 0
#         if self.vel > 0:
#             win.blit(self.enemySprite[self.walkCount//3], (self.x, self.y))
#             self.walkCount += 1
#         else:
#             win.blit(self.enemySprite[self.walkCount // 3], (self.x, self.y))
#             self.walkCount += 1
#         pass
#
#     def move(self):
#         if self.vel > 0:
#             if self.y + self.vel < self.path[1]:
#                 self.y += self.vel
#             else:
#                 self.vel = self.vel * -1
#                 self.walkCount = 0
#         else:
#             if self.y - self.vel > self.path[0]:
#                 self.y += self.vel
#             else:
#                 self.vel = self.vel * -1
#                 self.walkCount = 0
#         pass
#
# ## Continuar implmentando inimigo para ir na lista e desaparecer
# class AlienEnemy(object):
#     enemySprite = [pygame.image.load('Game/invader.gif')]
#
#
# bgnd = background(500, 480)
# win = bgnd.drawBackground()
# man = player(200, 410, 64, 64)
# goblin = enemy(random.randrange(70, 420), -70, 64, 64, 550)
#
#
#
#
# walkRight = [pygame.image.load('Game/ally.gif')]
# walkLeft = [pygame.image.load('Game/ally.gif')]
# char = pygame.image.load('Game/ally.gif')
# bg = pygame.image.load('Game/space_invaders_background.gif')
#
# clock = pygame.time.Clock()
#
#
# def redrawGameWindow():
#     win.blit(bg, (0, 0))
#     man.draw(win)
#     goblin.draw(win)
#     for bullet in bullets:
#         bullet.draw(win)
#
#     pygame.display.update()
#
#
# bullets = []
# run = True
# while run:
#     clock.tick(27)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#     for bullet in bullets:
#         if bullet.y < 500 and bullet.y > 0:
#             bullet.y -= bullet.vel
#         else:
#             bullets.pop(bullets.index(bullet))
#
#     keys = pygame.key.get_pressed()
#
#     if keys[pygame.K_SPACE]:
#         if len(bullets) < 1:
#             bullets.append(projectile(round(man.x + man.width//2), round(man.y + man.height//2), 6, (0, 0, 0)))
#
#     if keys[pygame.K_LEFT] and man.x > man.vel:
#         man.x -= man.vel
#         man.left = True
#         man.right = False
#         man.standing = False
#     elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
#         man.x += man.vel
#         man.right = True
#         man.left = False
#         man.standing = False
#     else:
#         man.standing = True
#         man.walkCount = 0
#
#     if not (man.isJump):
#         if keys[pygame.K_UP]:
#             man.isJump = True
#             man.right = False
#             man.left = False
#             man.walkCount = 0
#     else:
#         if man.jumpCount >= -10:
#             neg = 1
#             if man.jumpCount < 0:
#                 neg = -1
#             man.y -= (man.jumpCount ** 2) * 0.5 * neg
#             man.jumpCount -= 1
#         else:
#             man.isJump = False
#             man.jumpCount = 10
#
#     redrawGameWindow()
#
# pygame.quit()