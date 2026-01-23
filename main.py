import arcade

import math

from random import randint, choice
from enemies import *


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


class Game(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, fullscreen=True)
        arcade.set_background_color(arcade.color.COOL_BLACK)  # Библиотека arcade импортирована в файле enemies.py

        self.sprite_list = arcade.SpriteList()

        self.player = arcade.Sprite("pic/game_player.png", scale=1)
        self.player.center_x = 500
        self.player.center_y = 500
        self.player.speed = 5
        self.sprite_list.append(self.player)

        self.enemies_list = arcade.SpriteList()

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.enemies_list)
        self.enemies_generate()

    def enemies_generate(self):
        n = randint(6, 7)
        for _ in range(n):
            enemy = eval(f'{choice(get_enemies()).__name__}()')
            enemy.center_x = randint(0 + 100, 1920 - 100)
            enemy.center_y = randint(0 + 100, 1080 - 100)
            self.enemies_list.append(enemy)

    def on_draw(self):
        self.clear()
        self.sprite_list.draw()
        self.enemies_list.draw()

    def on_update(self, delta_time):
        if self.player.change_x != 0 or self.player.change_y != 0:
            self.player.angle = math.degrees(math.atan2(self.player.change_x, self.player.change_y))  # чудо формула :)
        for enemy in self.enemies_list:
            enemy.move(delta_time)
        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_y = self.player.speed
        elif key == arcade.key.S:
            self.player.change_y = -self.player.speed
        elif key == arcade.key.A:
            self.player.change_x = -self.player.speed
        elif key == arcade.key.D:
            self.player.change_x = self.player.speed

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.W, arcade.key.S]:
            self.player.change_y = 0
        if key in [arcade.key.A, arcade.key.D]:
            self.player.change_x = 0


if __name__ == '__main__':
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
