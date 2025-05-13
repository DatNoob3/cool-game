import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Image as Ball")

# Colors
white = (255, 255, 255)
green = (0, 128, 0)

# Load the ball image
try:
    ball_image = pygame.image.load("horse.png").convert_alpha()
    # Replace "your_ball_image.png" with the actual path to your image file.
    # .convert_alpha() is important for images with transparency.
except pygame.error as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    sys.exit()

# Get the dimensions of the image
ball_rect = ball_image.get_rect()
ball_rect.center = (width // 2, 50)  # Initial position

# Ball properties (we'll use the rect for position)
ball_speed_x = 0
ball_speed_y = 0
gravity = 0.5
horizontal_acceleration = 1
horizontal_deceleration = 0.9

# Platform properties
platform_height = 20
platform_width = 150
platform_x = (width - platform_width) // 2
platform_y = height - platform_height - 50

# Camera properties
camera_x = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player input for horizontal movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ball_speed_x -= horizontal_acceleration
    if keys[pygame.K_RIGHT]:
        ball_speed_x += horizontal_acceleration

    # Apply horizontal deceleration
    ball_speed_x *= horizontal_deceleration

    # Apply gravity
    ball_speed_y += gravity

    # Move the ball (using the rect)
    ball_rect.x += int(ball_speed_x)
    ball_rect.y += int(ball_speed_y)

    # Ball collision with left wall (elastic)
    if ball_rect.left < 0:
        ball_speed_x *= -1
        ball_rect.left = 0

    # Ball collision with top wall (elastic)
    if ball_rect.top < 0:
        ball_speed_y *= -1
        ball_rect.top = 0

    # Ball collision with platform (elastic)
    if ball_rect.bottom > platform_y and \
       ball_rect.right > platform_x - camera_x and \
       ball_rect.left < platform_x + platform_width - camera_x and \
       ball_speed_y > 0:
        ball_rect.bottom = platform_y
        ball_speed_y *= -1

    # Ball hits the bottom (elastic)
    elif ball_rect.bottom > height:
        ball_rect.bottom = height
        ball_speed_y *= -1
        ball_speed_x *= 1.0

    # Camera follow logic
    camera_speed = 5
    if ball_rect.centerx > width // 2 + 100 + camera_x:
        camera_x += ball_speed_x
    elif ball_rect.centerx < width // 2 - 100 + camera_x and camera_x > 0:
        camera_x += ball_speed_x

    # Clear the screen
    screen.fill(white)

    # Draw the ball image (relative to the camera)
    screen.blit(ball_image, (ball_rect.x - camera_x, ball_rect.y))

    # Draw the platform (relative to the camera)
    pygame.draw.rect(screen, green, (int(platform_x - camera_x), int(platform_y), platform_width, platform_height))

    # Update the display
    pygame.display.flip()

    # Control game speed
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()