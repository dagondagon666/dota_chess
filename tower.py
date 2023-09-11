from draw import draw_single_tile_unit


class Tower:
    def __init__(self, x, y, hp, color, name):
        self.x = x
        self.y = y
        self.hp = hp
        self.color = color
        self.name = name

    def attack(self, enemies):
        for enemy in enemies:
            if abs(self.x - enemy.x) <= 2 and abs(self.y - enemy.y) <= 2:
                enemy.hp -= 1
                if enemy.hp <= 0:
                    enemy.reset()

    def draw(self, window, tile_size):
        draw_single_tile_unit(
            window, self.color, self.x, self.y, tile_size, self.name, self.hp
        )
