import arcade  # Некоторые библиотеки горят серым, так как импортированы в других файлах

import math

from random import randint, choice
from arcade import check_for_collision_with_list
from enemies import *


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


class Game(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, fullscreen=False)
        arcade.set_background_color(arcade.color.COOL_BLACK)

        self.sprite_list = arcade.SpriteList()

        self.player = arcade.Sprite("pic/game_player.png", scale=1)
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player.speed = 10
        self.sprite_list.append(self.player)

        self.bullet_list = arcade.SpriteList()
        self.enemies_list = arcade.SpriteList()
        self.enemies_generate()

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.enemies_list)

        self.move = [0, 0]  # Движение игрока по оси x, y (скорость)

        self.fire = set()  # Список нажатых стрелочек, для ориентации пуль
        self.bullet_delay = 0.10  # Задержка выстрела пуль при зажатой кнопке
        self.bullet_speed = 25
        self.last_bullet_fired = 0  # Время прошедшее с последнего выстрела

    def enemies_generate(self):
        n = randint(4, 15)
        for _ in range(n):
            enemy = eval(f'{choice(get_enemies()).__name__}()')
            enemy.center_x = randint(0 + 100, 1920 - 100)
            enemy.center_y = randint(0 + 100, 1080 - 100)
            self.enemies_list.append(enemy)

    def on_draw(self):
        self.clear()
        self.sprite_list.draw()
        self.bullet_list.draw()
        self.enemies_list.draw()

    def on_update(self, delta_time):
        if self.player.change_x != 0 or self.player.change_y != 0:
            self.player.angle = math.degrees(math.atan2(self.player.change_x, self.player.change_y))  # чудо формула :)

        for enemy in self.enemies_list:
            enemy.move(delta_time)
            if check_for_collision_with_list(enemy, self.bullet_list):  # Удаление врага и пули при их столкновении
                check_for_collision_with_list(enemy, self.bullet_list)[0].remove_from_sprite_lists()
                enemy.remove_from_sprite_lists()

        for bullet in self.bullet_list:
            bullet.center_x += bullet.change_x
            bullet.center_y += bullet.change_y
            if bullet.bottom > SCREEN_HEIGHT or bullet.top < 0 or bullet.right < 0 or bullet.left > SCREEN_WIDTH:
                bullet.remove_from_sprite_lists()

        self.player.change_x, self.player.change_y = self.move[::1]

        if any(self.fire) and self.last_bullet_fired >= self.bullet_delay:  # Генерация пуль при зажатой кнопке
            bullet = arcade.Sprite(':resources:images/space_shooter/meteorGrey_small1.png', 0.5)
            bullet.center_x = self.player.center_x
            bullet.center_y = self.player.center_y
            for key in self.fire:
                if key == arcade.key.UP:
                    bullet.change_y = self.bullet_speed
                elif key == arcade.key.DOWN:
                    bullet.change_y = -self.bullet_speed
                elif key == arcade.key.LEFT:
                    bullet.change_x = -self.bullet_speed
                elif key == arcade.key.RIGHT:
                    bullet.change_x = self.bullet_speed
            self.bullet_list.append(bullet)
            self.last_bullet_fired = 0  # Сброс

        if not self.enemies_list:
            self.enemies_generate()

        self.last_bullet_fired += delta_time
        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.move[1] += self.player.speed
        elif key == arcade.key.S:
            self.move[1] -= self.player.speed
        elif key == arcade.key.A:
            self.move[0] -= self.player.speed
        elif key == arcade.key.D:
            self.move[0] += self.player.speed
        elif key in [arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT]:
            self.fire.add(key)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.move[1] -= self.player.speed
        elif key == arcade.key.S:
            self.move[1] += self.player.speed
        elif key == arcade.key.A:
            self.move[0] += self.player.speed
        elif key == arcade.key.D:
            self.move[0] -= self.player.speed
        self.fire.discard(key)


if __name__ == '__main__':
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
