import math
from arcade import check_for_collision_with_list
from enemies import *

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


class GameView(arcade.View):
    """Класс для представления игрового процесса"""

    def __init__(self):
        super().__init__()
        self.player = None
        self.player_speed = 10
        self.sprite_list = None
        self.bullet_list = None
        self.enemies_list = None
        self.physics_engine = None
        self.move = [0, 0]  # Движение игрока по оси x, y (скорость)
        self.fire = set()  # Список нажатых стрелочек, для ориентации пуль
        self.bullet_delay = 0.30  # Задержка выстрела пуль при зажатой кнопке
        self.bullet_speed = 25
        self.last_bullet_fired = 0  # Время прошедшее с последнего выстрела
        self.bg = arcade.Sprite('pic/background.png')
        self.bg_lst = arcade.SpriteList()

    def setup(self):
        """Инициализация игровых объектов"""
        self.bg.width = SCREEN_WIDTH
        self.bg.height = SCREEN_HEIGHT
        self.bg.center_x = SCREEN_WIDTH // 2
        self.bg.center_y = SCREEN_HEIGHT // 2
        self.bg_lst.append(self.bg)
        self.sprite_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemies_list = arcade.SpriteList()

        self.player = arcade.Sprite("pic/game_player.png", scale=1)
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.sprite_list.append(self.player)

        self.enemies_generate()

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.enemies_list)
        self.move = [0, 0]
        self.fire = set()
        self.last_bullet_fired = 0

    def enemies_generate(self):
        n = randint(4, 15)
        for _ in range(n):
            enemy_class = choice(get_enemies())
            enemy = enemy_class()
            enemy.center_x = randint(100, SCREEN_WIDTH - 100)
            enemy.center_y = randint(100, SCREEN_HEIGHT - 100)
            self.enemies_list.append(enemy)

    def on_draw(self):
        self.clear()
        self.bg_lst.draw()
        self.sprite_list.draw()
        self.bullet_list.draw()
        self.enemies_list.draw()
        arcade.draw_text(f"Врагов осталось: {len(self.enemies_list)}",
                         10, SCREEN_HEIGHT - 30,
                         arcade.color.WHITE, 20)

        arcade.draw_text("ESC - Главное меню",
                         SCREEN_WIDTH - 400, SCREEN_HEIGHT - 30,
                         arcade.color.GRAY, 20)

    def on_update(self, delta_time):

        if self.player.change_x != 0 or self.player.change_y != 0:
            self.player.angle = math.degrees(math.atan2(self.player.change_x, self.player.change_y))

        for enemy in self.enemies_list:
            enemy.move(delta_time, self.player.center_x, self.player.center_y, self.bullet_list)
            if check_for_collision_with_list(enemy, self.bullet_list):
                collided_bullets = check_for_collision_with_list(enemy, self.bullet_list)
                if collided_bullets:
                    collided_bullets[0].remove_from_sprite_lists()
                enemy.remove_from_sprite_lists()

        for bullet in self.bullet_list:
            bullet.center_x += bullet.change_x
            bullet.center_y += bullet.change_y
            if (bullet.bottom > SCREEN_HEIGHT or bullet.top < 0 or
                    bullet.right < 0 or bullet.left > SCREEN_WIDTH):
                bullet.remove_from_sprite_lists()

        self.player.change_x, self.player.change_y = self.move[0], self.move[1]

        if self.fire and self.last_bullet_fired >= self.bullet_delay:
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
            self.last_bullet_fired = 0

        if not self.enemies_list:
            self.enemies_generate()

        self.last_bullet_fired += delta_time
        self.physics_engine.update()

        if check_for_collision_with_list(self.player, self.enemies_list):
            from main_menu import MainMenuView
            menu_view = MainMenuView()
            self.window.show_view(menu_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.move[1] += self.player_speed
        elif key == arcade.key.S:
            self.move[1] -= self.player_speed
        elif key == arcade.key.A:
            self.move[0] -= self.player_speed
        elif key == arcade.key.D:
            self.move[0] += self.player_speed
        elif key in [arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT]:
            self.fire.add(key)
        elif key == arcade.key.ESCAPE:
            from main_menu import MainMenuView
            menu_view = MainMenuView()
            self.window.show_view(menu_view)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.move[1] -= self.player_speed
        elif key == arcade.key.S:
            self.move[1] += self.player_speed
        elif key == arcade.key.A:
            self.move[0] += self.player_speed
        elif key == arcade.key.D:
            self.move[0] -= self.player_speed
        self.fire.discard(key)

if __name__ == '__main__':
    from main_menu import MainMenuView

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Geometry Wars", fullscreen=False)
    menu_view = MainMenuView()
    window.show_view(menu_view)
    arcade.run()