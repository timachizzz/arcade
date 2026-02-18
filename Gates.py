import arcade
from math import cos, sin, radians
from random import randint, uniform

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


class Gate(arcade.Sprite):
    def __init__(self):
        super().__init__('pic/gate.png')
        self.scale = 1.0

        self.rotation_speed = uniform(30, 60)
        self.speed = uniform(50, 100)
        self.rotation_angle = randint(0, 360)
        self.move_angle = randint(0, 360)
        self.purify_area_radius = 300

        self.center_x = randint(100, SCREEN_WIDTH - 100)
        self.center_y = randint(100, SCREEN_HEIGHT - 100)

    def move(self, delta_time):
        """Обновление позиции и поворота ворот"""
        self.rotation_angle += self.rotation_speed * delta_time
        self.angle = self.rotation_angle % 360

        self.center_x += self.speed * cos(radians(self.move_angle)) * delta_time
        self.center_y += self.speed * sin(radians(self.move_angle)) * delta_time

        margin = 50
        if self.center_x < margin:
            self.move_angle = 180 - self.move_angle
            self.center_x = margin
        elif self.center_x > SCREEN_WIDTH - margin:
            self.move_angle = 180 - self.move_angle
            self.center_x = SCREEN_WIDTH - margin

        if self.center_y < margin:
            self.move_angle = -self.move_angle
            self.center_y = margin
        elif self.center_y > SCREEN_HEIGHT - margin:
            self.move_angle = -self.move_angle
            self.center_y = SCREEN_HEIGHT - margin

        self.move_angle %= 360

    def get_triangle_positions(self, triangle_width, triangle_height):

        half_gate_height = self.height / 2
        half_triangle_height = triangle_height / 2

        offset_distance = half_gate_height + half_triangle_height

        up_x = sin(radians(self.angle))
        up_y = cos(radians(self.angle))
        down_x = -up_x
        down_y = -up_y

        top_x = self.center_x + up_x * offset_distance
        top_y = self.center_y + up_y * offset_distance

        bottom_x = self.center_x + down_x * offset_distance
        bottom_y = self.center_y + down_y * offset_distance

        return (top_x, top_y), (bottom_x, bottom_y)


class DeathTriangle(arcade.Sprite):
    def __init__(self):
        super().__init__('pic/death_triangle.png')
        self.scale = 1.0
        self.angle = 0

    def update_position(self, x, y):
        self.center_x = x
        self.center_y = y
