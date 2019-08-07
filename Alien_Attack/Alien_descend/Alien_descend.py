import pygame
import random
import Alien_Attack.Alien_descend.Components as comp

pygame.init()


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



def game_loop():

    gameExit = False
    gameOver = False
    isdead = True
    shootLoop = 0
    score = 0
    bullets = []
    enemies = []

    bgnd = comp.my_background(500, 480)
    win = bgnd.drawBackground()
    man = comp.my_player(200, 410, 64, 64)
    goblin = 0


    while not gameExit:
        if isdead == True:
            new_goblin = comp.my_enemy(random.randrange(70, 420), 0, 64, 64, 480)
            goblin = new_goblin
            isdead = False

        keys = pygame.key.get_pressed()
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

        for bullet in bullets:
            col = comp.my_collision(0, 0, goblin.hitbox, bullet)
            if bullet.y < 500 and bullet.y > 0:
                bullet.y -= bullet.vel
                if comp.my_collision.isCollidingBullet(col) == 0:
                    bullets.pop(bullets.index(bullet))
                    alien.hit()
                    isdead = True
                    score += man.score()
            else:
                bullets.pop(bullets.index(bullet))

        # for alien in enemies:
        alien = goblin
        col2 = comp.my_collision(man.hitbox, alien.hitbox, 0, 0)
        if comp.my_collision.isCollidingEnemy(col2) == 0:
            health = man.hit()
            if health > 0:
                print("zpiurr!")
            else:
                gameOver = True
        # alien offscreen
        if goblin.y + goblin.height > 510:
            isdead = True



        if keys[pygame.K_SPACE] and shootLoop == 0:
            if len(bullets) < 5:
                bullets.append(comp.my_projectile(round(man.x + man.width//2), round(man.y + man.height//2), 6, (255, 255, 255)))

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

    pygame.quit()
    quit()

game_loop()
