from random import choice

import arcade


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


class Enemy(arcade.Sprite):
    def __init__(self, texture):
        super().__init__(texture)


class Square(Enemy):
    def __init__(self):
        super().__init__('pic/square.png')
        self.direction, self.act = choice(['center_x', 'center_y']), choice(['-=', '+='])
        self.speed = 50
        self.i = 0

    def move(self, delta_time):
        if self.i > 3 * 60:
            self.direction, self.act = choice(['center_x', 'center_y']), choice(['-=', '+='])
            self.i = 0
        exec(f'self.{self.direction} {self.act} {self.speed * delta_time}')
        if self.left <= 0 or self.bottom <= 0:
            self.act = '+='
        elif self.right >= SCREEN_WIDTH or self.top >= SCREEN_HEIGHT:
            self.act = '-='
        self.i += 1

# class Pinwheel(Enemy):
    # ...


# class Rocket(Enemy):
    # ...


def get_enemies():
    """Возвращает список всех противников (для появления на игровом поле)"""
    return Enemy.__subclasses__()
