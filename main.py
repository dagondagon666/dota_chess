import logging

import pygame

from base import Base
from hero import Hero
from tower import Tower
from game_state import GameState
from colors import *
import utils
import draw

pygame.init()

# LOGGING
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

# Constants
WIDTH, HEIGHT = 900, 1100
MAP_HEIGHT = HEIGHT - 200
TILE_SIZE = MAP_HEIGHT // 20
HAS_DISPLAY = True

# The button object for "End Turn"
attack_button = pygame.Rect(WIDTH - 400, HEIGHT - 100, 180, 60)
ability_button = pygame.Rect(WIDTH - 600, HEIGHT - 100, 180, 60)
end_turn_button = pygame.Rect(WIDTH - 200, HEIGHT - 100, 180, 60)

# Game State
GAME_STATE = GameState()


def draw_grid(window, tile_size, width, height):
    for x in range(0, width, tile_size):
        pygame.draw.line(window, (0, 0, 0), (x, 0), (x, height))
    for y in range(0, height, tile_size):
        pygame.draw.line(window, (0, 0, 0), (0, y), (width, y))


def is_base_tile(x, y):
    base_tiles = [
        (1, 1),
        (1, 2),
        (2, 1),
        (2, 2),
        (17, 17),
        (17, 16),
        (16, 17),
        (16, 16),
    ]
    return (x, y) in base_tiles


def is_valid_coordinate(tile_x, tile_y):
    return 0 <= tile_x <= 19 and 0 <= tile_y <= 19


def handle_attack(tile_x, tile_y):
    if is_valid_coordinate:
        GAME_STATE.get()["selected_hero"].attack(GAME_STATE, tile_x, tile_y)


def handle_ability(tile_x, tile_y):
    if is_valid_coordinate:
        GAME_STATE.get()["selected_hero"].ability(GAME_STATE, tile_x, tile_y)


def handle_move(tile_x, tile_y):
    if is_valid_coordinate:
        GAME_STATE.get()["selected_hero"].move(GAME_STATE, tile_x, tile_y)


def handle_end_turn():
    logging.info(f"Player {GAME_STATE.get()['current_player']}: end turn")
    self_towers = GAME_STATE.get()["towers"][0].values()
    self_heroes = GAME_STATE.get()["heroes"][0]
    enemy_heroes = GAME_STATE.get()["heroes"][1]
    # Tower attack
    if GAME_STATE.get()["current_player"] == 2:
        self_towers = GAME_STATE.get()["towers"][1].values()
        self_heroes = GAME_STATE.get()["heroes"][1]
        enemy_heroes = GAME_STATE.get()["heroes"][0]

    for tower in self_towers:
        tower.attack(enemy_heroes)
    for hero in enemy_heroes:
        hero.has_moved = False

    GAME_STATE.switch_player()


def draw_control_area(window):
    # You can draw a rectangle to visually separate the control panel area
    pygame.draw.rect(window, (200, 200, 200), (0, MAP_HEIGHT, WIDTH, 200))

    # End button
    pygame.draw.rect(window, (0, 200, 0), end_turn_button)
    font = pygame.font.Font(None, 36)
    button_label = font.render("End Turn", True, (255, 255, 255))
    window.blit(button_label, (WIDTH - 180, HEIGHT - 80))

    # attack button
    if GAME_STATE.get()["selected_hero"]:
        pygame.draw.rect(window, RED, attack_button)
    else:
        pygame.draw.rect(window, RED_2, attack_button)
    attack_label = font.render("Attack", True, (255, 255, 255))
    window.blit(attack_label, (WIDTH - 380, HEIGHT - 80))

    # Ability button
    if GAME_STATE.get()["selected_hero"]:
        pygame.draw.rect(window, BLUE, ability_button)
    else:
        pygame.draw.rect(window, BLUE_2, ability_button)
    ability_label = font.render("Ability", True, (255, 255, 255))
    window.blit(ability_label, (WIDTH - 580, HEIGHT - 80))




def get_fog_of_war(window):
    visible_tiles = set()
    for unit in GAME_STATE.get_current_player_units():
        for dx in range(-5, 6):
            for dy in range(-5, 6):
                x, y = unit.x + dx, unit.y + dy
                if (
                    0 <= x <= 19
                    and 0 <= y <= 19
                    and utils.manhattan_distance(x, y, unit.x, unit.y) <= 5
                ):
                    visible_tiles.add((x, y))
    return visible_tiles


# Initialize Pygame window and clock
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    clock.tick(60)  # Limit the game to 60 frames per second
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Game logic here
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if GAME_STATE.get()["show_winner_overlay"]:
                logging.info("RESET Game")
                GAME_STATE.init_game_state()
            else:
                # Get tile coordinates of the clicked position
                x, y = event.pos
                tile_x, tile_y = x // TILE_SIZE, 19 - y // TILE_SIZE
                logging.info(
                    f"Player {GAME_STATE.get()['current_player']}: clicked ({tile_x}, {tile_y})"
                )

                ## Buttons
                ### End button
                if end_turn_button.collidepoint(x, y):
                    handle_end_turn()
                    continue
                ### attack button
                elif (
                    attack_button.collidepoint(x, y)
                    and GAME_STATE.get()["selected_hero"]
                ):
                    logging.info(
                        f"Player {GAME_STATE.get()['current_player']}: selected action ATTACK"
                    )
                    GAME_STATE.get()["selected_action"] = "attack"
                    continue
                ### Ability button
                elif (
                    ability_button.collidepoint(x, y)
                    and GAME_STATE.get()["selected_hero"]
                ):
                    logging.info(
                        f"Player {GAME_STATE.get()['current_player']}: selected action ABILITY"
                    )
                    GAME_STATE.get()["selected_action"] = "ability"
                    continue

                # Inside the main loop, within the MOUSEBUTTONDOWN event handling
                if GAME_STATE.get()["selected_hero"]:
                    if (
                        tile_x == GAME_STATE.get()["selected_hero"].x
                        and tile_y == GAME_STATE.get()["selected_hero"].y
                    ):
                        GAME_STATE.deselect_hero()
                        continue
                    if GAME_STATE.get()["selected_action"] == "attack":
                        handle_attack(tile_x, tile_y)
                    elif GAME_STATE.get()["selected_action"] == "ability":
                        handle_ability(tile_x, tile_y)
                    elif GAME_STATE.get()["selected_action"] == "move":
                        handle_move(tile_x, tile_y)
                else:
                    for hero in (
                        GAME_STATE.get()["heroes"][0]
                        if GAME_STATE.get()["current_player"] == 1
                        else GAME_STATE.get()["heroes"][1]
                    ):
                        if hero.x == tile_x and hero.y == tile_y and not hero.has_moved:
                            GAME_STATE.get()["selected_hero"] = hero
                            logging.info(
                                f"Player {GAME_STATE.get()['current_player']}: selected hero {GAME_STATE.get()['selected_hero'].name}"
                            )
                            break

    # Win Condition
    if GAME_STATE.get()["bases"][0].hp <= 0 or GAME_STATE.get()["bases"][1].hp <= 0:
        GAME_STATE.get()["winner"] = (
            "Player 2" if GAME_STATE.get()["bases"][0].hp <= 0 else "Player 1"
        )
        GAME_STATE.get()["show_winner_overlay"] = True

    # Update GameState Overview
    GAME_STATE.update_board()

    # Drawing
    if HAS_DISPLAY:
        window.fill(WHITE)

        draw_control_area(window)

        draw.paint_background(window, TILE_SIZE)

        draw.draw_highlighted_tiles(window, GAME_STATE, TILE_SIZE)

        visible_tiles = get_fog_of_war(window)
        for x in range(20):
            for y in range(20):
                if (x, y) not in visible_tiles:
                    draw.paint_fog_of_war_effect(window, x, y, TILE_SIZE)

        draw_grid(window, TILE_SIZE, WIDTH, MAP_HEIGHT)

        for hero in GAME_STATE.get()["heroes"][0] + GAME_STATE.get()["heroes"][1]:
            if (hero.x, hero.y) in visible_tiles:
                hero.draw(window, TILE_SIZE)

        for base in GAME_STATE.get()["bases"]:
            base.draw(window, TILE_SIZE)
        for tower in list(GAME_STATE.get()["towers"][0].values()) + list(
            GAME_STATE.get()["towers"][1].values()
        ):
            tower.draw(window, TILE_SIZE)

        if GAME_STATE.get()["show_winner_overlay"]:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            window.blit(overlay, (0, 0))

            font = pygame.font.Font(None, 74)
            winner_label = font.render(
                f"{GAME_STATE.get()['winner']} Won!", True, (255, 255, 255)
            )
            window.blit(
                winner_label,
                (
                    WIDTH // 2 - winner_label.get_width() // 2,
                    HEIGHT // 2 - winner_label.get_height() // 2,
                ),
            )

        pygame.display.flip()  # Update the display

pygame.quit()
