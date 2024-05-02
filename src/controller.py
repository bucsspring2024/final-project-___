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
game_won = False  # Variable to track if the game is won

font = pygame.font.Font(None, 36)

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


def display_text(text, font, size, color, x, y):
    font = pygame.font.Font(font, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    win.blit(text_surface, text_rect)


def get_dad_joke():
    api_url = 'https://api.api-ninjas.com/v1/dadjokes'
    headers = {'X-Api-Key': '3uTiWvkQdf+fmg69kZBJ/g==Brlqg9EuDrgCodAY'}
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        jokes = response.json()
        if jokes:  # Check if jokes list is not empty
            joke = jokes[0]  # Select the first joke from the list
            return joke
        else:
            return None
    else:
        return None


# Example usage:
dad_joke = get_dad_joke()
if dad_joke:
    print(dad_joke['joke'])
else:
    print("Failed to fetch dad joke.")




# Function to display the winning screen

def winning_screen():
    global game_won
    win.fill(WHITE)
    display_text("Congratulations! You won!", None, 40, (0, 0, 0), win_width // 2, win_height // 2 - 50)
    # Display the dad joke without dictionary formatting
    dad_joke_str = dad_joke['joke']
    display_text(dad_joke_str, None, 30, (0, 0, 0), win_width // 2, win_height // 2 + 50)
    # Additional text
    additional_text = "The monsters heard the joke and went back to where they came from. The end!!!"
    display_text(additional_text, None, 30, (0, 0, 0), win_width // 2, win_height // 2 + 100)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()






class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
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
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/MenuBackground.png")


def get_font(size):  # Returns Press-Start-2P in the desired size
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


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 350),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return True  # Signal to start the game
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


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
        self.y = y + 200
        self.velx = 10
        self.vely = 10
        self.face_right = True
        self.face_left = False
        self.stepIndex = 0
        self.jump = False
        self.width = 35
        self.height = 48
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hitbox = (self.x, self.y, 32, 50)

    def move_hero(self, userInput):
        if userInput[pygame.K_RIGHT] and self.x <= win_width - 62:
            self.x += self.velx
            self.rect.x = self.x
            self.face_right = True
            self.face_left = False
        elif userInput[pygame.K_LEFT] and self.x >= 0:
            self.x -= self.velx
            self.rect.x = self.x
            self.face_right = False
            self.face_left = True
        else:
            self.stepIndex = 0

    def draw(self, win, color=None):
        self.hitbox = (self.x, self.y, 32, 50)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 1)
        if self.stepIndex >= 9:
            self.stepIndex = 0
        if color is not None:
            # Create a surface with the same size as the hero image
            colored_surface = pygame.Surface((self.width, self.height))
            colored_surface.fill(color)  # Fill the surface with the specified color
            if self.face_left:
                # Blit the colored surface and hero image onto the window
                win.blit(colored_surface, (self.x, self.y))
                win.blit(left_resized[self.stepIndex], (self.x, self.y))
                self.stepIndex += 1
            if self.face_right:
                # Blit the colored surface and hero image onto the window
                win.blit(colored_surface, (self.x, self.y))
                win.blit(right_resized[self.stepIndex], (self.x, self.y))
                self.stepIndex += 1
        else:
            # Draw the hero without coloring
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
            self.y -= self.vely * 4
            self.rect.y = self.y
            self.vely -= 1
        if self.vely < -10:
            self.jump = False
            self.vely = 10

    def direction(self):
        if self.face_right:
            return 1
        if self.face_left:
            return -1




class Enemy(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.image.load('assets/Enemy.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.player = player  # Store the player object
        # Initialize enemy position
        self.rect.center = (random.randint(0, 1280), 100)  # Fixed y-coordinate
        self.dx = random.choice([-1, 1])  # Randomly choose initial direction
        self.bullet_cooldown = 0
        self.bullet_cooldown_max = 20  # Adjust the frequency of shooting

    def update(self):
        # Move side to side within screen boundaries
        self.rect.x += self.dx * 2  # Adjust speed as needed
        # Change direction if reaching screen edges
        if self.rect.left < 0 or self.rect.right > 1280:
            self.dx *= -1
            self.rect.x += self.dx * 2  # Move back to stay within bounds

        # Decrease cooldown each frame
        self.bullet_cooldown -= 1

        # Check if cooldown is over and shoot bullet
        if self.bullet_cooldown <= 0:
            # Choose random angle for bullet direction
            angle = random.choice([0, math.pi/4, -math.pi/4])  # 0 for straight down, pi/4 for 45 degrees, -pi/4 for -45 degrees
            # Calculate bullet velocity components based on angle
            vel_x = math.sin(angle) * 5  # Adjust speed as needed
            vel_y = math.cos(angle) * 5  # Adjust speed as needed
            bullet = Bullet(self.rect.centerx, self.rect.bottom, vel_x, vel_y, speed=3, player=self.player)  # Pass the player object
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.bullet_cooldown = self.bullet_cooldown_max

    def draw(self, win):
        win.blit(self.image, self.rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, vel_x, vel_y, speed, player):
        super().__init__()
        self.image = pygame.Surface((5, 5))  # Create a simple square bullet
        self.image.fill((255, 0, 0))  # Fill the bullet with red color
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # Set initial position of the bullet
        self.vel_x = vel_x  # Velocity components
        self.vel_y = vel_y
        self.speed = speed  # Bullet speed
        self.player = player

    def update(self):
        # Move the bullet according to its velocity and speed
        self.rect.x += self.vel_x * self.speed
        self.rect.y += self.vel_y * self.speed

        # Remove the bullet if it goes off the screen
        if self.rect.y > win_height:
            self.kill()

        if pygame.sprite.collide_rect(self, self.player):
            self.kill()  # Remove the bullet

    def draw(self, win):  # Define the draw method to render the bullet
        win.blit(self.image, self.rect)


class Game:
    def __init__(self):
        self.background_x = 0
        self.player = Hero(250, 400)
        self.enemies = pygame.sprite.Group()  # Group to store all enemies

        # Create multiple enemies
        for _ in range(10):
            enemy = Enemy(self.player)
            self.enemies.add(enemy)

    def draw_game(self, player):
        global background_x
        self.background_x -= 1
        if self.background_x <= -win_width:
            self.background_x = 0

        win.fill((0, 0, 0))
        win.blit(background, (self.background_x, 0))
        win.blit(background, (self.background_x + win_width, 0))

        player.draw(win)

        self.enemies.update()  # Update all enemies
        self.enemies.draw(win)  # Draw all enemies

        bullets.update()  # Update all bullets
        bullets.draw(win)  # Draw all bullets

        pygame.time.delay(30)
        pygame.display.update()


# Define the game over screen function
def game_over_screen():
    while True:
        # Display game over text and options
        SCREEN.fill("black")
        game_over_text = get_font(50).render("Game Over", True, "White")
        game_over_rect = game_over_text.get_rect(center=(640, 260))
        SCREEN.blit(game_over_text, game_over_rect)

        # Add retry and close buttons
        retry_button = Button(image=None, pos=(640, 420), text_input="Retry", font=get_font(50), base_color="White", hovering_color="Green")
        close_button = Button(image=None, pos=(640, 520), text_input="Close", font=get_font(50), base_color="White", hovering_color="Red")

        retry_button.update(SCREEN)
        close_button.update(SCREEN)

        # Check for input from the user
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.checkForInput(pygame.mouse.get_pos()):
                    # Restart the game
                    main()
                elif close_button.checkForInput(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()



def main():
    global game_over, game_won, hero_flashing

    if main_menu():
        game_instance = Game()
        player = Hero(250, 400)
        start_time = pygame.time.get_ticks()  # Record the start time

        run = True
        while run:
            current_time = pygame.time.get_ticks()  # Get the current time
            elapsed_time = (current_time - start_time) / 1000  # Convert milliseconds to seconds

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            userInput = pygame.key.get_pressed()

            player.move_hero(userInput)
            player.jump_motion(userInput)

            game_instance.draw_game(player)

            # Check for collisions between hero and bullets
            if pygame.sprite.spritecollideany(player, bullets):
                game_over = True
                # Display game over screen
                game_over_screen()
                # Exit the game loop
                run = False

            # Check if 10 seconds have elapsed
            if elapsed_time >= 15:
                game_won = True
                # Display winning screen
                winning_screen()
                # Exit the game loop
                run = False

            
            # Check if the game is won
            if game_won:
                winning_screen()  # Display the winning screen
                run = False  # Exit the game loop when the game is won



if __name__ == "__main__":
    main()
    pygame.quit()