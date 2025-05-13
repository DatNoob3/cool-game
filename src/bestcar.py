import pygame
import sys

# ─── Configuration ─────────────────────────────────────────────────────────────
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
CAR_SIZE = (40, 60)
TRACK_COLOR = (50, 50, 50)
EDGE_COLOR  = (200, 200, 200)

# ─── Car Class ─────────────────────────────────────────────────────────────────
class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path="car.png"):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (80, 160))  # Adjust size as needed
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(self.rect.center)
        self.vel = pygame.math.Vector2(0, 0)
        self.angle = 0
        self.acceleration = 0.2
        self.max_speed = 20
        self.turn_speed = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.vel += pygame.math.Vector2(0, -self.acceleration).rotate(self.angle)
        if keys[pygame.K_DOWN]:
            self.vel *= 0.9
        if keys[pygame.K_RIGHT]:
            self.angle += self.turn_speed
        if keys[pygame.K_LEFT]:
            self.angle -= self.turn_speed

        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)

        self.pos += self.vel

        # 🔁 Fix distorted rotation
        self.image = pygame.transform.rotozoom(self.original_image, -self.angle, 1)
        self.rect = self.image.get_rect(center=self.pos)



# ─── Main Game ────────────────────────────────────────────────────────────────
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Top-Down Racing Template")
    clock = pygame.time.Clock()
	
    camera_offset = pygame.Vector2(0, 0)


    # Sprite groups
    all_sprites = pygame.sprite.Group()
    player = Car(SCREEN_WIDTH//2, SCREEN_HEIGHT-100)
    all_sprites.add(player)

    # Track boundaries (simple example: two vertical lines)
    track_edges = [
        pygame.Rect(100, 0, 10, SCREEN_HEIGHT),
        pygame.Rect(SCREEN_WIDTH-110, 0, 10, SCREEN_HEIGHT)
    ]

    running = True
    while running:
        # ─── Event Handling ─────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # ─── Update ────────────────────────────────────────────────
        all_sprites.update()
        camera_offset.x = player.pos.x - SCREEN_WIDTH // 2
        camera_offset.y = player.pos.y - SCREEN_HEIGHT // 2


        # ─── Collision with edges ─────────────────────────────────
        for edge in track_edges:
            if player.rect.colliderect(edge):
                player.vel *= -0.5  # simple bounce/back-off

        # ─── Draw ─────────────────────────────────────────────────
        screen.fill((34, 139, 34))  # grass

        # Draw track
        track_rect = pygame.Rect(100 - camera_offset.x, -camera_offset.y, SCREEN_WIDTH - 200, SCREEN_HEIGHT * 2)
        pygame.draw.rect(screen, TRACK_COLOR, track_rect)

        # Draw edges
        for edge in track_edges:
            edge_moved = edge.move(-camera_offset)
            pygame.draw.rect(screen, EDGE_COLOR, edge_moved)

        # Draw car manually (skip all_sprites.draw())
        for sprite in all_sprites:
            screen.blit(sprite.image, sprite.rect.move(-camera_offset))


        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()