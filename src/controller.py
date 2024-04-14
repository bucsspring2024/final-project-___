import pygame
import os
import random

pygame.init()


screen = pygame.display.set_mode((1000,500)) #screen = win
backGroundPath = "assets/BackGround.png"
backGround = pygame.image.load(backGroundPath)
bg = pygame.transform.scale(backGround, (1000,500))
pygame.display.set_caption("Leon's Game")
i = 0
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    
    #background
    screen.fill((0,0,0))
    screen.blit(bg, (i, 0))
    screen.blit(bg, (1000+i, 0))

    if i == -1000:
        screen.blit(bg, (1000+i, 0))
        i = 0

    i -= 1


    #Character Boundary and movement
    x = 250
    y = 250
    vel_x = 10
    vel_y = 10
    jump = False


    userInput = pygame.key.get_pressed()
    if userInput[pygame.K_LEFT] and x > 0:
        x -= vel_x
    if userInput[pygame.K_RIGHT] and x < 1000:
        x += vel_x
    if userInput[pygame.K_UP] and y > 0:
        y -= vel_y
    if userInput[pygame.K_DOWN] and y < 500:
        y += vel_y

    if jump is False and userInput[pygame.K_SPACE]:
        jump = True

    if jump is True:
        y -= vel_y
        vel_y -= 1
        if vel_y < -10:
            jump = False
            vel_y = 10
    
#character animation
stationary = pygame.image.load("assets/Character/M.png")

# One way to do it - using the sprites that face left.
left =  [pygame.image.load(os.path.join("Assets/Hero", "L1.png")),
         pygame.image.load(os.path.join("Assets/Hero", "L2.png")),
         pygame.image.load(os.path.join("Assets/Hero", "L3.png")),
         pygame.image.load(os.path.join("Assets/Hero", "L4.png")),
         pygame.image.load(os.path.join("Assets/Hero", "L5.png")),
         pygame.image.load(os.path.join("Assets/Hero", "L6.png")),
         pygame.image.load(os.path.join("Assets/Hero", "L7.png")),
         pygame.image.load(os.path.join("Assets/Hero", "L8.png")),
         pygame.image.load(os.path.join("Assets/Hero", "L9.png"))]


right = [None]*10
for picIndex in range(1,10):
    right[picIndex-1] = pygame.image.load(os.path.join("Assets/Hero", "R" + str(picIndex) + ".png"))
    picIndex+=1

pygame.time.delay(10)
pygame.display.update()
