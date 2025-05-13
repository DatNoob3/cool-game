import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Camera Following Ball")

# Colors
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 128, 0)

# Ball properties
ball_radius = 15
ball_x = width // 2
ball_y = 50
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
camera_x = 0  # Initial camera offset

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

    # Move the ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Ball collision with left wall (elastic)
    if ball_x - ball_radius < 0:
        ball_speed_x *= -1
        ball_x = ball_radius

    # Ball collision with top wall (elastic)
    if ball_y - ball_radius < 0:
        ball_speed_y *= -1
        ball_y = ball_radius

    # Ball collision with platform (elastic)
    if ball_y + ball_radius > platform_y and \
       ball_x + ball_radius > platform_x - camera_x and \
       ball_x - ball_radius < platform_x + platform_width - camera_x and \
       ball_speed_y > 0:
        ball_y = platform_y - ball_radius
        ball_speed_y *= -1

    # Ball hits the bottom (elastic)
    elif ball_y + ball_radius > height:
        ball_y = height - ball_radius
        ball_speed_y *= -1
        ball_speed_x *= 1.0

    # Camera follow logic
    camera_speed = 5  # Adjust for how quickly the camera follows
    if ball_x > width // 2 + 100 + camera_x:  # If ball moves past a certain point on the right
        camera_x += ball_speed_x # Or += camera_speed for constant follow speed
    elif ball_x < width // 2 - 100 + camera_x and camera_x > 0: # If ball moves past a certain point on the left and camera is not at the start
        camera_x += ball_speed_x # Or -= camera_speed for constant follow speed

    # Keep camera within reasonable bounds (optional, for a finite world)
    # if camera_x < 0:
    #     camera_x = 0
    # elif camera_x > world_width - width: # Assuming you have a world_width defined
    #     camera_x = world_width - width

    # Clear the screen
    screen.fill(white)

    # Draw the ball (relative to the camera)
    pygame.draw.circle(screen, blue, (int(ball_x - camera_x), int(ball_y)), ball_radius)

    # Draw the platform (relative to the camera)
    pygame.draw.rect(screen, green, (int(platform_x - camera_x), int(platform_y), platform_width, platform_height))

    # Update the display
    pygame.display.flip()

    # Control game speed
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()