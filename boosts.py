import arcade

from enemies import SCREEN_WIDTH, SCREEN_HEIGHT
from math import sin, cos, radians
from random import randint


GLITCHING_TIME = 0.055  # Период смены текстур при пропадании


class Doubler(arcade.Sprite):
    def __init__(self):
        super().__init__('pic/doubler.png')
        self.image = arcade.load_image('pic/doubler.png')
        self.scale = 0.2
        self.speed = 50
        self.move_angle = randint(0, 360)
        self.rotation_angle = 0
        self.rotation_speed = 200
        self.original_image = self.image.copy()
        self.center_x = randint(80, SCREEN_WIDTH - 60)
        self.center_y = randint(80, SCREEN_HEIGHT - 60)
        self.lifetime = 5

        self.delay = 0
        self.i = 0
        self.textures = [self.texture, arcade.load_texture('pic/empty.png')]
        self.normal_texture = self.texture

    def move(self, delta_time):
        self.rotation_angle += self.rotation_speed * delta_time
        self.angle = self.rotation_angle % 360
        self.rotation_angle += self.rotation_speed * delta_time
        self.center_x += self.speed * cos(radians(self.move_angle)) * delta_time
        self.center_y += self.speed * sin(radians(self.move_angle)) * delta_time

        if self.left < 0:
            self.move_angle = 180 - self.move_angle
        elif self.right > SCREEN_WIDTH - self.width:
            self.move_angle = 180 - self.move_angle
        if self.bottom < 0:
            self.move_angle = -self.move_angle
        elif self.top > SCREEN_HEIGHT - self.height:
            self.move_angle = -self.move_angle
        self.move_angle %= 360

    def _update(self, delta_time):
        self.lifetime -= delta_time
        if 0 <= self.lifetime <= 2:
            self.delay += delta_time
            if self.delay >= GLITCHING_TIME:
                self.delay = 0
                self.i += 1
                self.texture = self.textures[self.i % 2]
        elif self.lifetime < 0:
            self.remove_from_sprite_lists()
