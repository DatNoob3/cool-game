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
    def __init__(self, x, y, color=(255,0,0)):
        super().__init__()
        # Simple rectangle as a placeholder car
        self.original_image = pygame.Surface(CAR_SIZE)
        self.original_image.fill(color)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(self.rect.center)
        self.vel = pygame.math.Vector2(0, 0)
        self.angle = 0
        self.acceleration = 0.2
        self.max_speed = 5
        self.turn_speed = 3

    def update(self):
        keys = pygame.key.get_pressed()
        # accelerate/brake
        if keys[pygame.K_UP]:
            self.vel += pygame.math.Vector2(0, -self.acceleration).rotate(self.angle)
        if keys[pygame.K_DOWN]:
            self.vel *= 0.9  # simple friction/brake

        # turn
        if keys[pygame.K_LEFT]:
            self.angle += self.turn_speed
        if keys[pygame.K_RIGHT]:
            self.angle -= self.turn_speed

        # limit speed
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)

        # update position
        self.pos += self.vel
        self.rect.center = self.pos

        # rotate image
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)


# ─── Main Game ────────────────────────────────────────────────────────────────
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Top-Down Racing Template")
    clock = pygame.time.Clock()

    # Sprite groups
    all_sprites = pygame.sprite.Group()
    player = Car(SCREEN_WIDTH//2, SCREEN_HEIGHT-100, color=(0,200,0))
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

        # ─── Collision with edges ─────────────────────────────────
        for edge in track_edges:
            if player.rect.colliderect(edge):
                player.vel *= -0.5  # simple bounce/back-off

        # ─── Draw ─────────────────────────────────────────────────
        screen.fill((34, 139, 34))  # grass
        pygame.draw.rect(screen, TRACK_COLOR, (100, 0, SCREEN_WIDTH-200, SCREEN_HEIGHT))
        for edge in track_edges:
            pygame.draw.rect(screen, EDGE_COLOR, edge)

        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()