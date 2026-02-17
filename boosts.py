import arcade

from enemies import SCREEN_WIDTH, SCREEN_HEIGHT
from math import sin, cos, radians
from random import randint


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

    def move(self, delta_time):
        self.rotation_angle += self.rotation_speed * delta_time
        self.angle = self.rotation_angle % 360
        self.rotation_angle += self.rotation_speed * delta_time
        self.center_x += self.speed * cos(radians(self.move_angle)) * delta_time
        self.center_y += self.speed * sin(radians(self.move_angle)) * delta_time

        if self.center_x < 50:
            self.move_angle = 180 - self.move_angle

        elif self.center_x > SCREEN_WIDTH - 50:
            self.move_angle = 180 - self.move_angle

        if self.center_y < 50:
            self.move_angle = -self.move_angle

        elif self.center_y > SCREEN_HEIGHT - 50:
            self.move_angle = -self.move_angle

        self.move_angle %= 360