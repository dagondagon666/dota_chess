import pygame


class Base:
    def __init__(self, x, y, hp, color, name):
        self.x = x
        self.y = y
        self.hp = hp
        self.color = color
        self.name = name

    def draw(self, window, tile_size):
        pygame.draw.rect(
            window,
            self.color,
            (
                self.x * tile_size,
                (18 - self.y) * tile_size,
                tile_size * 2,
                tile_size * 2,
            ),
        )
        font = pygame.font.Font(None, 33)
        name_label = font.render(f"{self.name}", True, (0, 0, 0))
        hp_label = font.render(f"{self.hp} HP", True, (0, 0, 0))

        window.blit(name_label, (self.x * tile_size + 5, (18 - self.y) * tile_size + 5))
        window.blit(
            hp_label, (self.x * tile_size + 5, (18 - self.y) * tile_size + 38)
        )  # Adjust Y-offset as needed
