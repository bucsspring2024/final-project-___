import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Enemy Shooting Example")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))  # Red
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.image.load('assets/Enemy.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.player = player
        # Initialize enemy position
        self.rect.center = (random.randint(0, SCREEN_WIDTH), self.player.rect.centery - 200)
        self.dx = random.choice([-1, 1])  # Randomly choose initial direction

    def update(self):
        # Move side to side within screen boundaries
        self.rect.x += self.dx * 2  # Adjust speed as needed
        # Change direction if reaching screen edges
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.dx *= -1
            self.rect.x += self.dx * 2  # Move back to stay within bounds

        # Shoot at the player
        if random.randint(1, 100) == 1:  # Adjust frequency of shooting
            bullet = Bullet(self.rect.center, self.player.rect.center)
            all_sprites.add(bullet)
            bullets.add(bullet)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, start, target):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = start
        self.speed = 5
        self.dx = target[0] - start[0]
        self.dy = target[1] - start[1]
        self.dist = max(abs(self.dx), abs(self.dy))
        if self.dist != 0:
            self.rect.x += self.dx / self.dist * self.speed
            self.rect.y += self.dy / self.dist * self.speed

    def update(self):
        # Move towards the target
        if self.dist != 0:
            self.rect.x += self.dx / self.dist * self.speed
            self.rect.y += self.dy / self.dist * self.speed

# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create enemies
for _ in range(5):
    enemy = Enemy(player)
    all_sprites.add(enemy)
    enemies.add(enemy)

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Draw
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
