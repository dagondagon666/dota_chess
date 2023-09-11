import pygame

from colors import *

import utils

TILE_BACKGROUND_MAP = {}
TILE_LABEL_MAP = {}

for x in range(20):
    for y in range(20):
        if x + y < 17:
            TILE_BACKGROUND_MAP[(x, y)] = "green"
        else:
            TILE_BACKGROUND_MAP[(x, y)] = "red"
# add river
for x in range(20):
    TILE_BACKGROUND_MAP[(x, 19 - x)] = "river"
for x in range(10):
    TILE_BACKGROUND_MAP[(x, 18 - x)] = "river"
for x in range(11, 20):
    TILE_BACKGROUND_MAP[(x, 20 - x)] = "river"

# add trees
for x in range(20):
    TILE_LABEL_MAP[(0, x)] = "tree"
    TILE_LABEL_MAP[(19, x)] = "tree"
    TILE_LABEL_MAP[(x, 0)] = "tree"
    TILE_LABEL_MAP[(19, x)] = "tree"
print(f"tree #: {len(TILE_LABEL_MAP)}")

def draw_single_tile_unit(window, color, x, y, tile_size, name, hp):
    paint_single_tile(window, color, x, y, tile_size)
    font = pygame.font.Font(None, 20)  # Adjust font size as needed
    name_label = font.render(f"{name}", True, (0, 0, 0))
    hp_label = font.render(f"{hp} HP", True, (0, 0, 0))

    window.blit(name_label, (x * tile_size + 5, (19 - y) * tile_size + 5))
    window.blit(hp_label, (x * tile_size + 5, (19 - y) * tile_size + 25))


def paint_single_tile(window, color, x, y, tile_size):
    pygame.draw.rect(
        window,
        color,
        (x * tile_size, (19 - y) * tile_size, tile_size, tile_size),
    )


def label_single_tile(window, label, color, x, y, tile_size, font):
    label = font.render(label, True, color)
    window.blit(label, (x * tile_size + 15, (19 - y) * tile_size + 15))


def image_single_tile(window, image, x, y, tile_size):
    icon_image = pygame.image.load(image)
    icon_image = pygame.transform.scale(icon_image, (tile_size, tile_size))
    window.blit(icon_image, (x * tile_size, (19 - y) * tile_size))


def paint_background(window, tile_size):
    for x in range(20):
        for y in range(20):
            color = GREEN_GRASSY
            if TILE_BACKGROUND_MAP[(x, y)] == "red":
                color = RED_5
            elif TILE_BACKGROUND_MAP[(x, y)] == "river":
                color = BLUE_DODGER
            paint_single_tile(window, color, x, y, tile_size)
            if (x, y) in TILE_LABEL_MAP:
                if TILE_LABEL_MAP[(x, y)] == "tree":
                    image_single_tile(window, "./images/tree.png", x, y, tile_size)

def paint_fog_of_war_effect(window, x, y, tile_size):
    start_pos = (x * tile_size, (19 - y) * tile_size)
    end_pos = ((x + 1) * tile_size, (20 - y) * tile_size)
    pygame.draw.line(window, (0, 0, 0), start_pos, end_pos, 5)
    pygame.draw.line(
        window, (0, 0, 0), (start_pos[0], end_pos[1]), (end_pos[0], start_pos[1]), 5
    )

def draw_highlighted_tiles(window, game_state, tile_size):
    if game_state.get()["selected_hero"]:
        selected_hero = game_state.get()["selected_hero"]
        highlighted_tiles = [
            (x, y)
            for x in range(selected_hero.x - 5, selected_hero.x + 6)
            for y in range(selected_hero.y - 5, selected_hero.y + 6)
            if utils.manhattan_distance(x, y, selected_hero.x, selected_hero.y) <= 5
            and 0 <= x <= 19
            and 0 <= y <= 19
        ]

        for x, y in highlighted_tiles:
            pygame.draw.rect(
                window,
                BLUE_LIGHT,
                (x * tile_size, (19 - y) * tile_size, tile_size, tile_size),
            )