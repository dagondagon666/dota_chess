import logging

from draw import draw_single_tile_unit

from tower import Tower
import utils


class Hero:
    def __init__(self, x, y, max_hp, color, name, max_move=5, attack=1, attack_range = 1):
        self.x = x
        self.y = y
        self.spawn_x = x
        self.spawn_y = y
        self.hp = max_hp
        self.max_hp = max_hp
        self.max_move = max_move
        self.color = color
        self.name = name
        
        self.attack_dmg = attack

        self.has_moved = False

    def move(self, game_state, x, y):
        if utils.manhattan_distance(self.x, self.y, x, y) <= self.max_move:
            self.x = x
            self.y = y
            self.has_moved = True
            logging.info(
                f"Player {game_state.get()['current_player']}: Moved hero {game_state.get()['selected_hero'].name} -> {x}, {y}"
            )
        game_state.deselect_hero()

    def attack(self, game_state, x, y):
        if utils.manhattan_distance(self.x, self.y, x, y) <= 5:
            target = game_state.get_target(x, y)
            if target:
                target_old_hp = target.hp
                target.hp -= 1
                if target.hp <= 0:
                    if isinstance(target, Hero):
                        target.reset()
                    elif isinstance(target, Tower):
                        game_state.destroy_tower(target.name)

                game_state.get()[
                    "selected_action"
                ] = "move"  # Reset action to move after performing attack
                self.has_moved = True
                logging.info(
                    f"Player {game_state.get()['current_player']}: hero {game_state.get()['selected_hero'].name} ATTACKED enemy {target.name}: {target_old_hp} -> {target.hp}"
                )
            elif not target:  # If it's not a base tile, move the hero
                self.x = x
                self.y = y
                self.has_moved = True
                logging.info(
                    f"Player {game_state.get()['current_player']}: Attack Moved hero {game_state.get()['selected_hero'].name} -> {x}, {y}"
                )
        game_state.deselect_hero()

    def ability(self, game_state, x, y):
        if utils.manhattan_distance(self.x, self.y, x, y) <= 5:
            target = game_state.get_target(
                x,
                y,
            )
            if target and isinstance(target, Hero):
                target_hero_old_hp = target.hp
                target.hp = round(target.hp / 2)
                game_state.get()[
                    "selected_action"
                ] = "move"  # Reset action to move after using ability
                self.has_moved = True
                logging.info(
                    f"Player {game_state.get()['current_player']}: hero {game_state.get()['selected_hero'].name} used ABILITY on enemy hero {target.name}: {target_hero_old_hp} -> {target.hp}"
                )
            elif not target:  # If it's an empty place, move the hero
                self.x = x
                self.y = y
                self.has_moved = True
                logging.info(
                    f"Player {game_state.get()['current_player']}: Ability Moved hero {game_state.get()['selected_hero'].name} -> {x}, {y}"
                )
        game_state.deselect_hero()

    def reset(self):
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.hp = self.max_hp

    def draw(self, window, tile_size):
        color = self.color
        if self.has_moved:
            color = tuple(int(c * 0.5) for c in self.color)
        draw_single_tile_unit(
            window, color, self.x, self.y, tile_size, self.name, self.hp
        )
