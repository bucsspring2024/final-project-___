import pygame
import os

pygame.init()
win_height = 500
win_width = 1000
win = pygame.display.set_mode((win_width, win_height))

# Load and Size Images
# Hero (Player)
# Load the character images
left = [pygame.image.load(os.path.join("assets/Character", "L1.png")),
        pygame.image.load(os.path.join("assets/Character", "L2.png")),
        pygame.image.load(os.path.join("assets/Character", "L3.png")),
        pygame.image.load(os.path.join("assets/Character", "L4.png")),
        pygame.image.load(os.path.join("assets/Character", "L5.png")),
        pygame.image.load(os.path.join("assets/Character", "L6.png")),
        pygame.image.load(os.path.join("assets/Character", "L7.png")),
        pygame.image.load(os.path.join("assets/Character", "L8.png")),
        pygame.image.load(os.path.join("assets/Character", "L9.png"))
        ]

right = [pygame.image.load(os.path.join("assets/Character", "R1.png")),
         pygame.image.load(os.path.join("assets/Character", "R2.png")),
         pygame.image.load(os.path.join("assets/Character", "R3.png")),
         pygame.image.load(os.path.join("assets/Character", "R4.png")),
         pygame.image.load(os.path.join("assets/Character", "R5.png")),
         pygame.image.load(os.path.join("assets/Character", "R6.png")),
         pygame.image.load(os.path.join("assets/Character", "R7.png")),
         pygame.image.load(os.path.join("assets/Character", "R8.png")),
         pygame.image.load(os.path.join("assets/Character", "R9.png"))
         ]

character_width = 35
character_height = 48

left_resized = [pygame.transform.scale(image, (character_width, character_height)) for image in left]
right_resized = [pygame.transform.scale(image, (character_width, character_height)) for image in right]

background = pygame.transform.scale(pygame.image.load(os.path.join("assets", "BackGround.png")), (win_width, win_height))

class Hero:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velx = 10
        self.vely = 10
        self.face_right = True
        self.face_left = False
        self.stepIndex = 0
        self.jump = False

    def move_hero(self, userInput):
        if userInput[pygame.K_RIGHT] and self.x <= win_width - 62:
            self.x += self.velx
            self.face_right = True
            self.face_left = False
        elif userInput[pygame.K_LEFT] and self.x >= 0:
            self.x -= self.velx
            self.face_right = False
            self.face_left = True
        else:
            self.stepIndex = 0

    def draw(self, win):
        if self.stepIndex >= 9:
            self.stepIndex = 0
        if self.face_left:
            win.blit(left_resized[self.stepIndex], (self.x, self.y))
            self.stepIndex += 1
        if self.face_right:
            win.blit(right_resized[self.stepIndex], (self.x, self.y))
            self.stepIndex += 1

    def jump_motion(self, userInput):
        if userInput[pygame.K_SPACE] and self.jump is False:
            self.jump = True
        if self.jump:
            self.y -= self.vely*4
            self.vely -= 1
        if self.vely < -10:
            self.jump = False
            self.vely = 10

    def direction(self):
        if self.face_right:
            return 1
        if self.face_left:
            return -1

# Draw Game
class Game:
    def __init__(self):
        self.background_x = 0

    def draw_game(self, player):
        global background_x
        self.background_x -= 1
        if self.background_x <= -win_width:
            self.background_x = 0
        
        win.fill((0, 0, 0))
        # Draw the background
        win.blit(background, (self.background_x, 0))
        win.blit(background, (self.background_x + win_width, 0))

        # Draw player
        player.draw(win)
        
        pygame.time.delay(30)
        pygame.display.update()


def main():
    game_instance = Game()
    player = Hero(250,400)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        userInput = pygame.key.get_pressed()

        player.move_hero(userInput)
        player.jump_motion(userInput)

        game_instance.draw_game(player)

    pygame.quit()


if __name__ == "__main__":
    main()
