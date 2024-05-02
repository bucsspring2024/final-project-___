import pygame
import requests

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dad Joke Display")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Function to display text on the screen
def display_text(text, font, size, color, x, y):
    font = pygame.font.Font(font, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Fetch dad joke from API
api_url = 'https://api.api-ninjas.com/v1/dadjokes'
response = requests.get(api_url, headers={'X-Api-Key': '3uTiWvkQdf+fmg69kZBJ/g==Brlqg9EuDrgCodAY'})

if response.status_code == requests.codes.ok:
    dad_jokes = response.json()
    print(dad_jokes)  # Print out the response to examine its structure
    dad_joke = dad_jokes[0]["joke"]  # Assuming the jokes are in a list
else:
    dad_joke = "Error: Unable to fetch dad joke"

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white color
    screen.fill(WHITE)

    # Display dad joke on the screen
    display_text(dad_joke, None, 24, BLACK, screen_width // 2, screen_height // 2)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()

