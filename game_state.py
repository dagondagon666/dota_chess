import logging

from base import Base
from hero import Hero
from tower import Tower
from colors import *

HERO_HP = 10
BASE_HP = 5
TOWER_HP = 1


class GameState:
    def __init__(self) -> None:
        self.init_game_state()

    def init_game_state(self) -> None:
        self.game_state = {
            "heroes": [
                [
                    Hero(0, 0, HERO_HP, GREEN_2, 1),
                    Hero(0, 1, HERO_HP, GREEN_2, 2),
                    Hero(1, 0, HERO_HP, GREEN_2, 3),
                    Hero(0, 2, HERO_HP, GREEN_2, 4),
                    Hero(2, 0, HERO_HP, GREEN_2, 5),
                ],
                [
                    Hero(19, 19, HERO_HP, RED_2, 6),
                    Hero(19, 18, HERO_HP, RED_2, 7),
                    Hero(18, 19, HERO_HP, RED_2, 8),
                    Hero(19, 17, HERO_HP, RED_2, 9),
                    Hero(17, 19, HERO_HP, RED_2, 10),
                ],
            ],
            "bases": [
                Base(1, 1, BASE_HP, GREEN, "GREEN"),
                Base(17, 17, BASE_HP, RED, "RED"),
            ],
            "towers": [
                {
                    "GBT1": Tower(1, 14, TOWER_HP, GREEN, "GBT1"),
                    "GMT1": Tower(8, 8, TOWER_HP, GREEN, "GMT1"),
                    "GTT1": Tower(16, 1, TOWER_HP, GREEN, "GTT1"),
                    "GBT2": Tower(1, 10, TOWER_HP + 1, GREEN, "GBT2"),
                    "GMT2": Tower(6, 6, TOWER_HP + 1, GREEN, "GMT2"),
                    "GTT2": Tower(11, 1, TOWER_HP + 1, GREEN, "GTT2"),
                    "GBT3": Tower(1, 6, TOWER_HP + 2, GREEN, "GBT3"),
                    "GMT3": Tower(4, 4, TOWER_HP + 2, GREEN, "GMT3"),
                    "GTT3": Tower(6, 1, TOWER_HP + 2, GREEN, "GTT3"),
                    "GBT4": Tower(2, 3, TOWER_HP + 3, GREEN, "GBT4"),
                    "GTT4": Tower(3, 2, TOWER_HP + 3, GREEN, "GTT4"),
                },
                {
                    "RTT1": Tower(3, 18, TOWER_HP, RED, "RTT1"),
                    "RMT1": Tower(11, 11, TOWER_HP, RED, "RMT1"),
                    "RBT1": Tower(18, 5, TOWER_HP, RED, "RBT1"),
                    "RTT2": Tower(8, 18, TOWER_HP + 1, RED, "RTT2"),
                    "RMT2": Tower(13, 13, TOWER_HP + 1, RED, "RMT2"),
                    "RBT2": Tower(18, 9, TOWER_HP + 1, RED, "RBT2"),
                    "RTT3": Tower(13, 18, TOWER_HP + 2, RED, "RTT3"),
                    "RMT3": Tower(15, 15, TOWER_HP + 2, RED, "RMT3"),
                    "RBT3": Tower(18, 13, TOWER_HP + 2, RED, "RBT3"),
                    "RTT4": Tower(16, 17, TOWER_HP + 3, RED, "RTT4"),
                    "RBT4": Tower(17, 16, TOWER_HP + 3, RED, "RBT4"),
                },
            ],
            "current_player": 1,
            "hero_moved": [],
            "selected_hero": None,
            "selected_action": "move",
            "show_winner_overlay": False,
        }
        self.update_board()

    def deselect_hero(self):
        logging.info(
            f"Player {self.game_state['current_player']}: deselect hero {self.game_state['selected_hero'].name}"
        )
        self.game_state["selected_hero"] = None

    def get(self):
        return self.game_state

    def get_attr(self, key):
        return self.game_state[key]

    def get_current_player(self):
        return self.game_state["current_player"]

    def destroy_tower(self, name):
        towers = self.game_state["towers"][1]
        if self.get_current_player() == 2:
            towers = self.game_state["towers"][0]
        del towers[name]

    def get_target(self, x, y):
        heroes = self.game_state["heroes"][1]
        towers = self.game_state["towers"][1]
        base = self.game_state["bases"][1]
        if self.get_current_player() == 2:
            heroes = self.game_state["heroes"][0]
            towers = self.game_state["towers"][0]
            base = self.game_state["bases"][0]
        for hero in heroes:
            if hero.x == x and hero.y == y:
                return hero
        for tower in towers.values():
            if tower.x == x and tower.y == y:
                return tower
        if base.x == x and base.y == y:
            return base
        return None

    def switch_player(self):
        if self.get_current_player() == 1:
            self.game_state["current_player"] = 2
        else:
            self.game_state["current_player"] = 1
        logging.info(f"Game State: Switch to {self.game_state['current_player']}")

    def get_current_player_units(self):
        heroes = self.game_state["heroes"][0]
        towers = self.game_state["towers"][0]
        bases = self.game_state["bases"][0]
        if self.get_current_player() == 2:
            heroes = self.game_state["heroes"][1]
            towers = self.game_state["towers"][1]
            bases = self.game_state["bases"][1]
        return heroes + list(towers.values()) + [bases]

    def update_board(self):
        board = {}
        for i in range(2):
            for hero in self.game_state["heroes"][i]:
                board[(hero.x, hero.y)] = hero
            for tower in self.game_state["towers"][i].values():
                board[(tower.x, tower.y)] = tower
            base = self.game_state["bases"][i]
            board[(base.x, base.y)] = base
        self.game_state["board"] = board