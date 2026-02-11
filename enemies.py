from random import choice, randint, random
from math import sin, cos, radians, sqrt, atan2, degrees
import arcade
from arcade import SpriteList

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


class Enemy(arcade.Sprite):
    def __init__(self, texture):
        super().__init__(texture)


class DodgingEnemy(arcade.Sprite):
    def __init__(self, texture):
        super().__init__(texture)
        self.detection_area = 150
        self.dodge_speed = 100
        self.dodge_duration = 0
        self.bullet_list : list
        self.dodge_direction : list = []
        self.normal_move_timer = 0

    def check_for_bullets(self, bullet_list : SpriteList, delta_time):
        nearby_bullets : list = []
        for bullet in bullet_list:
            bullet_distance_x = bullet.center_x - self.center_x
            bullet_distance_y = bullet.center_y - self.center_y
            distance = sqrt(bullet_distance_x ** 2 + bullet_distance_y ** 2)

            if distance < self.detection_area:
                nearby_bullets.append((bullet, distance, bullet_distance_x, bullet_distance_y))

        return nearby_bullets

    def dodge(self, bullet_info, delta_time):
        if not bullet_info:
            self.dodge_duration = 0
            return

        closest_bullet = min(bullet_info, key=lambda x: x[1])
        bullet, distance, dx, dy = closest_bullet

        if distance > 0:
            dx_norm = dx / distance
            dy_norm = dy / distance
            if self.center_x < SCREEN_WIDTH // 2:
                dodge_dx = -dy_norm
                dodge_dy = dx_norm
            else:
                dodge_dx = dy_norm
                dodge_dy = -dx_norm

            dodge_force = 40
            self.center_x += dodge_dx * self.dodge_speed * delta_time * dodge_force
            self.center_y += dodge_dy * self.dodge_speed * delta_time * dodge_force

            self.dodge_duration = 0.3
            self.normal_move_timer = 0.2

class Square(Enemy):
    def __init__(self):
        super().__init__('pic/square.png')
        self.direction, self.act = choice(['center_x', 'center_y']), choice(['-=', '+='])
        self.speed = 300
        self.i = 0

    def move(self, delta_time, x, y, bullet):
        if self.i > 60:
            self.direction, self.act = choice(['center_x', 'center_y']), choice(['-=', '+='])
            self.i = 0
        exec(f'self.{self.direction} {self.act} {self.speed * delta_time}')
        if self.left <= 0 or self.bottom <= 0:
            self.act = '+='
        elif self.right >= SCREEN_WIDTH or self.top >= SCREEN_HEIGHT:
            self.act = '-='
        self.i += 1

class Pinwheel(Enemy):
    def __init__(self):
        super().__init__('pic/Pinwheel.png')
        self.image = arcade.load_image('pic/Pinwheel.png')
        self.scale = 1.0
        self.speed = 150
        self.move_angle = randint(0, 360)
        self.rotation_angle = 0
        self.rotation_speed = 200
        self.original_image = self.image.copy()
        self.center_x = randint(80, SCREEN_WIDTH - 60)
        self.center_y = randint(80, SCREEN_HEIGHT - 60)

    def move(self, delta_time, x, y, bullet):
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

class Rocket(Enemy):
    def __init__(self):
        super().__init__('pic/rocket.png')
        self.image = arcade.load_image('pic/rocket.png')
        self.scale = 1.2
        self.speed = 300
        self.angle = 0
        self.original_image = self.image.copy()
        self.center_x = randint(50, SCREEN_WIDTH - 50)
        self.center_y = randint(50, SCREEN_HEIGHT - 50)
        self.direction = choice([
            [1, 0],
            [-1, 0],
            [0, 1],
            [0, -1]
        ])
        self.update_rotation()

    def update_rotation(self):
        """Обновляет угол поворота в зависимости от направления"""
        if self.direction == [1, 0]:  # вправо
            self.angle = 90
        elif self.direction == [-1, 0]:  # влево
            self.angle = -90
        elif self.direction == [0, 1]:  # вниз
            self.angle = 0
        elif self.direction == [0, -1]:  # вверх
            self.angle = 180

    def move(self, delta_time, x, y, bullet):
        self.center_x += self.direction[0] * self.speed * delta_time
        self.center_y += self.direction[1] * self.speed * delta_time

        if self.left <= 0: #левый край
            self.direction[0] = 1 # вправо
            self.update_rotation()
        elif self.right >= SCREEN_WIDTH: # правый край
            self.direction[0] = -1 # влево
            self.update_rotation()
        if self.top <= 100: # нижний край
            self.direction[1] = 1 #вверх
            self.update_rotation()
        elif self.bottom >= SCREEN_HEIGHT - 80: # верхний край
            self.direction[1] = -1 # вниз
            self.update_rotation()


class Rhombus(Enemy):
    def __init__(self):
        super().__init__('pic/Romb.png')

        self.image = arcade.load_image('pic/Romb.png')
        self.scale = 1.0
        self.speed = 200
        self.center_x = randint(80, SCREEN_WIDTH - 60)
        self.center_y = randint(80, SCREEN_HEIGHT - 60)

    def move(self, delta_time, player_x=None, player_y=None, bullet=None):
        if player_x and player_y:
            delta_x = player_x - self.center_x
            delta_y = player_y - self.center_y
            distance = sqrt(delta_x ** 2 + delta_y ** 2)
            if distance > 0:
                self.center_x += (delta_x / distance) * delta_time * self.speed
                self.center_y += (delta_y / distance) * delta_time * self.speed
            else:
                self.center_x += self.speed / 10 * delta_time
                self.center_y += self.speed / 10 * delta_time


class DodgingRhombus(DodgingEnemy):
    def __init__(self):
        super().__init__('pic/Rombo.png')
        self.image = arcade.load_image('pic/Rombo.png')
        self.scale = 1.0
        self.speed = 250
        self.detection_area = 200
        self.dodge_speed = 375
        self.center_x = randint(50, SCREEN_WIDTH - 50)
        self.center_y = randint(50, SCREEN_HEIGHT - 50)
        self.normal_move_timer = 0
        self.dodge_duration = 0
        self.dodge_move_duration = 0
        self.dodge_angle = 0
        self.dodge_vector = [0, 0]  # Вектор уклонения

    def get_safe_direction(self, bullet_dx, bullet_dy):
        """Возвращает безопасное направление для уклонения"""
        # Угол направления на пулю
        bullet_angle = degrees(atan2(bullet_dy, bullet_dx))

        options = [
            (bullet_angle + 90) % 360,
            (bullet_angle - 90) % 360,
            (bullet_angle + 180) % 360,
        ]

        # Уклонение в случайном направлении
        if random() < 0.5:
            options.append((bullet_angle + 135) % 360)
            options.append((bullet_angle + 225) % 360)
        else:
            options.append((bullet_angle + 45) % 360)
            options.append((bullet_angle + 315) % 360)

        return choice(options)

    def dodge_with_angle(self, bullet_info, delta_time):
        if not bullet_info:
            self.dodge_duration = 0
            self.dodge_move_duration = 0
            return

        closest_bullet = min(bullet_info, key=lambda x: x[1])
        bullet, distance, dx, dy = closest_bullet

        self.dodge_angle = self.get_safe_direction(dx, dy)

        self.dodge_vector[0] = cos(radians(self.dodge_angle))
        self.dodge_vector[1] = sin(radians(self.dodge_angle))

        dodge_time = 0.2
        if distance < 100:
            dodge_time = 0.4
        elif distance < 150:
            dodge_time = 0.3

        self.dodge_move_duration = dodge_time
        self.dodge_duration = 0.4
        self.normal_move_timer = 0.1

    def move(self, delta_time, player_x, player_y, bullet_list):
        nearby_bullets = self.check_for_bullets(bullet_list, delta_time)

        if nearby_bullets and self.dodge_duration <= 0:
            self.dodge_with_angle(nearby_bullets, delta_time)

        if self.dodge_move_duration > 0:
            # Плавное ускорение
            speed_multiplier = 1.0
            if self.dodge_move_duration > 0.2:
                speed_multiplier = 2.0
            elif self.dodge_move_duration > 0.1:
                speed_multiplier = 1.8
            else:
                speed_multiplier = 1.4

            self.center_x += self.dodge_vector[0] * self.dodge_speed * delta_time * speed_multiplier
            self.center_y += self.dodge_vector[1] * self.dodge_speed * delta_time * speed_multiplier
            self.dodge_move_duration -= delta_time
        else:
            if self.dodge_duration > 0:
                self.dodge_duration -= delta_time

            if self.normal_move_timer > 0:
                self.normal_move_timer -= delta_time

            if self.normal_move_timer <= 0 and player_x and player_y:
                delta_x = player_x - self.center_x
                delta_y = player_y - self.center_y
                distance = sqrt(delta_x ** 2 + delta_y ** 2)
                if distance > 0:
                    self.center_x += (delta_x / distance) * self.speed * delta_time
                    self.center_y += (delta_y / distance) * self.speed * delta_time

        self.center_x = max(50, min(SCREEN_WIDTH - 50, self.center_x))
        self.center_y = max(50, min(SCREEN_HEIGHT - 50, self.center_y))


def get_enemies():
    """Возвращает список всех противников (для появления на игровом поле)"""
    return Enemy.__subclasses__() + DodgingEnemy.__subclasses__()
