import pygame
import os
import sys
import random
import math
import requests

from pygame.sprite import Group

pygame.init()
win_height = 720
win_width = 1280
win = pygame.display.set_mode((win_width, win_height))
all_sprites = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
game_over = False
game_won = False 
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")
BG = pygame.image.load("assets/MenuBackground.png")

font = pygame.font.Font(None, 36)

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

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


def display_text(text, font, size, color, x, y):
    """
    Display text on the screen.

    Args:
        text (str): The text to display.
        font (str): The path to the font file.
        size (int): The size of the font.
        color (tuple): The color of the text as a tuple of RGB values.
        x (int): The x-coordinate of the center of the text.
        y (int): The y-coordinate of the center of the text.
    """
    font = pygame.font.Font(font, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    win.blit(text_surface, text_rect)



def get_dad_joke():
    """
    Retrieve a dad joke from an external API.

    Returns:
        dict: A dictionary containing the dad joke.
            Example: {'id': '123', 'joke': 'Why couldn't the bicycle stand up by itself? It was two-tired.'}
        None: If the API request fails or no joke is found.
    """
    api_url = 'https://api.api-ninjas.com/v1/dadjokes'
    headers = {'X-Api-Key': '3uTiWvkQdf+fmg69kZBJ/g==Brlqg9EuDrgCodAY'}
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        jokes = response.json()
        if jokes:
            joke = jokes[0]
            return joke
    return None



def winning_screen():
    """
    Display the winning screen.

    Retrieves a dad joke from an external API and displays it along with a congratulatory message and additional text.

    """
    dad_joke = get_dad_joke()
    global game_won
    win.fill(WHITE)
    display_text("Congratulations! You won!", None, 40, (0, 0, 0), win_width // 2, win_height // 2 - 50)
    dad_joke_str = dad_joke['joke']
    display_text(dad_joke_str, None, 30, (0, 0, 0), win_width // 2, win_height // 2 + 50)
    additional_text = "The monsters heard the joke cringed and went back to where they came from. The end!!!"
    display_text(additional_text, None, 30, (0, 0, 0), win_width // 2, win_height // 2 + 100)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()






class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        """
        Initialize a Button object.

        Args:
            image (pygame.Surface or None): The image to display on the button.
                If None, the button will display text only.
            pos (tuple): The position of the button as a tuple of (x, y) coordinates.
            text_input (str): The text to display on the button.
            font (str): The path to the font file.
            base_color (tuple): The base color of the button as a tuple of RGB values.
            hovering_color (tuple): The color of the button when hovered over as a tuple of RGB values.
        """
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        """
        Update the button's appearance on the screen.

        Args:
            screen (pygame.Surface): The surface where the button will be drawn.
        """
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        """
        Check if a given position is within the button's area.

        Args:
            position (tuple): The position to check as a tuple of (x, y) coordinates.

        Returns:
            bool: True if the position is within the button's area, False otherwise.
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def change_color(self, position):
        """
        Change the button's text color based on the mouse position.

        Args:
            position (tuple): The position of the mouse as a tuple of (x, y) coordinates.
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)



def get_font(size):
    """
    Returns the Press-Start-2P font in the desired size.

    Args:
        size (int): The desired size of the font.

    Returns:
        pygame.font.Font: The Press-Start-2P font object with the specified size.
    """
    return pygame.font.Font("assets/font.ttf", size)


def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460),
                           text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def play():
    """
    Main function for the PLAY screen.
    """
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460),
                           text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.change_color(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.check_for_input(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    """
    Main function for the Dodge the Bullets screen.
    """
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(60).render("Dodge the Bullets!!!", True, (255,0,0))
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 350),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.change_color(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.check_for_input(MENU_MOUSE_POS):
                    return True 
                if QUIT_BUTTON.check_for_input(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()




class Hero:
    def __init__(self, x, y):
        """
        Initializes the Hero object.

        Args:
            x (int): The x-coordinate of the Hero's starting position.
            y (int): The y-coordinate of the Hero's starting position.
        """
        self.x = x
        self.y = y + 200
        self.velx = 10
        self.vely = 10
        self.face_right = True
        self.face_left = False
        self.step_index = 0
        self.jump = False
        self.width = 35
        self.height = 48
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hitbox = (self.x, self.y, 32, 50)

    def move_hero(self, user_input):
        """
        Moves the Hero based on user input.

        Args:
            user_input (dict): A dictionary containing the user's keyboard input.
        """
        if user_input[pygame.K_RIGHT] and self.x <= win_width - 62:
            self.x += self.velx
            self.rect.x = self.x
            self.face_right = True
            self.face_left = False
        elif user_input[pygame.K_LEFT] and self.x >= 0:
            self.x -= self.velx
            self.rect.x = self.x
            self.face_right = False
            self.face_left = True
        else:
            self.step_index = 0

    def draw(self, win, color=None):
        """
        Draws the Hero on the window.

        Args:
            win: The window surface to draw on.
            color (tuple): The color to fill the Hero with (optional).
        """
        self.hitbox = (self.x, self.y, 32, 50)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 1)
        if self.step_index >= 9:
            self.step_index = 0
        if color is not None:
            colored_surface = pygame.Surface((self.width, self.height))
            colored_surface.fill(color)
            if self.face_left:
                win.blit(colored_surface, (self.x, self.y))
                win.blit(left_resized[self.step_index], (self.x, self.y))
                self.step_index += 1
            if self.face_right:
                win.blit(colored_surface, (self.x, self.y))
                win.blit(right_resized[self.step_index], (self.x, self.y))
                self.step_index += 1
        else:
            if self.face_left:
                win.blit(left_resized[self.step_index], (self.x, self.y))
                self.step_index += 1
            if self.face_right:
                win.blit(right_resized[self.step_index], (self.x, self.y))
                self.step_index += 1

    def jump_motion(self, user_input):
        """
        Implements the jumping motion of the Hero.

        Args:
            user_input (dict): A dictionary containing the user's keyboard input.
        """
        if user_input[pygame.K_SPACE] and self.jump is False:
            self.jump = True
        if self.jump:
            self.y -= self.vely * 4
            self.rect.y = self.y
            self.vely -= 1
        if self.vely < -10:
            self.jump = False
            self.vely = 10

    def direction(self):
        """
        Determines the direction the Hero is facing.

        Returns:
            int: 1 if facing right, -1 if facing left.
        """
        if self.face_right:
            return 1
        if self.face_left:
            return -1





class Enemy(pygame.sprite.Sprite):
    def __init__(self, player):
        """
        Initializes the Enemy object.

        Args:
            player (Hero): The player object.
        """
        super().__init__()
        self.image = pygame.image.load('assets/Enemy.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.player = player 
        self.rect.center = (random.randint(0, 1280), 100) 
        self.dx = random.choice([-1, 1])
        self.bullet_cooldown = 0
        self.bullet_cooldown_max = 20  

    def update(self):
        """
        Updates the state of the enemy.
        """
        self.rect.x += self.dx * 2 
        if self.rect.left < 0 or self.rect.right > 1280:
            self.dx *= -1
            self.rect.x += self.dx * 2  

        self.bullet_cooldown -= 1


        if self.bullet_cooldown <= 0:
            angle = random.choice([0, math.pi/4, -math.pi/4])  # 0 for straight down, pi/4 for 45 degrees, -pi/4 for -45 degrees
            # Calculate bullet velocity components based on angle
            vel_x = math.sin(angle) * 5 
            vel_y = math.cos(angle) * 5  
            bullet = Bullet(self.rect.centerx, self.rect.bottom, vel_x, vel_y, speed=3, player=self.player) 
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.bullet_cooldown = self.bullet_cooldown_max

    def draw(self, win):
        """
        Draws the enemy on the window.

        Args:
            win: The window surface to draw on.
        """
        win.blit(self.image, self.rect)



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, vel_x, vel_y, speed, player):
        """
        Initializes the Bullet object.

        Args:
            x (int): Initial x-coordinate of the bullet.
            y (int): Initial y-coordinate of the bullet.
            vel_x (float): Velocity component along the x-axis.
            vel_y (float): Velocity component along the y-axis.
            speed (int): Bullet speed.
            player (Hero): The player object.
        """
        super().__init__()
        self.image = pygame.Surface((5, 5)) 
        self.image.fill((255, 0, 0)) 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  
        self.vel_x = vel_x 
        self.vel_y = vel_y
        self.speed = speed  
        self.player = player

    def update(self):
        """
        Updates the state of the bullet.
        """

        self.rect.x += self.vel_x * self.speed
        self.rect.y += self.vel_y * self.speed

        if self.rect.y > win_height:
            self.kill()

        if pygame.sprite.collide_rect(self, self.player):
            self.kill()  

    def draw(self, win):
        """
        Draws the bullet on the window.

        Args:
            win: The window surface to draw on.
        """
        win.blit(self.image, self.rect)


class Game:
    def __init__(self):
        """
        Initializes the Game object.
        """
        self.background_x = 0
        self.player = Hero(250, 400)
        self.enemies = pygame.sprite.Group()  


        for _ in range(10):
            enemy = Enemy(self.player)
            self.enemies.add(enemy)

    def draw_game(self, player):
        """
        Draws the game screen.

        Args:
            player (Hero): The player object.
        """
        global background_x
        self.background_x -= 1
        if self.background_x <= -win_width:
            self.background_x = 0

        win.fill((0, 0, 0))
        win.blit(background, (self.background_x, 0))
        win.blit(background, (self.background_x + win_width, 0))

        player.draw(win)

        self.enemies.update()  
        self.enemies.draw(win)  

        bullets.update()  
        bullets.draw(win) 

        pygame.time.delay(30)
        pygame.display.update()


def game_over_screen():
    """
    Displays the game over screen and handles user input.
    """
    while True:
        SCREEN.fill("black")
        game_over_text = get_font(50).render("Game Over", True, "White")
        game_over_rect = game_over_text.get_rect(center=(640, 260))
        SCREEN.blit(game_over_text, game_over_rect)

        retry_button = Button(image=None, pos=(640, 420), text_input="Retry", font=get_font(50), base_color="White", hovering_color="Green")
        close_button = Button(image=None, pos=(640, 520), text_input="Close", font=get_font(50), base_color="White", hovering_color="Red")

        retry_button.update(SCREEN)
        close_button.update(SCREEN)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.check_for_input(pygame.mouse.get_pos()):
                    controller = Controller() 
                    controller.main_loop()  
                elif close_button.check_for_input(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()



class Controller:
    def main_loop(self):
        """
        Main loop of the game.
        """
        global game_over, game_won

        if main_menu():
            game_instance = Game()
            player = Hero(250, 400)
            start_time = pygame.time.get_ticks() 

            run = True
            while run:
                current_time = pygame.time.get_ticks() 
                elapsed_time = (current_time - start_time) / 1000  

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                user_input = pygame.key.get_pressed()

                player.move_hero(user_input)
                player.jump_motion(user_input)

                game_instance.draw_game(player)

                if pygame.sprite.spritecollideany(player, bullets):
                    game_over = True
                    game_over_screen()
                    run = False

                if elapsed_time >= 15:
                    game_won = True
                    winning_screen()
                    run = False

                if game_won:
                    winning_screen()  
                    run = False  


