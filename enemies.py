from random import choice, randint
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

    def move(self, delta_time):
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

def get_enemies():
    """Возвращает список всех противников (для появления на игровом поле)"""
    return Enemy.__subclasses__()
