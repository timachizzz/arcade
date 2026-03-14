import math

import arcade.color
from arcade import check_for_collision_with_list
from pyglet.graphics import Batch

import particles
from enemies import *
from boosts import *
from loaded_music import *
from GameOverScreen import GameOverView


SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()
CAMERA_SMOOTHNESS = 0.15


class Evolved(arcade.View):
    """Класс для представления игрового процесса"""

    def __init__(self):
        super().__init__()
        self.player = None
        self.player_speed = 10
        self.lives, self.bombs = 0, 0
        self.activated_bombs = []
        self.sprite_list = None
        self.bullet_list = None
        self.enemies_list = None
        self.non_touchable_enemies_list = None
        self.physics_engine = None
        self.alive = True
        self.batch = Batch()
        self.score = None
        self.highscore = None
        self.file_scores = None
        self.move = [0, 0]  # Движение игрока по оси x, y (скорость)
        self.fire = set()  # Список нажатых стрелочек, для ориентации пуль
        self.bullet_delay = 0.15  # Задержка выстрела пуль при зажатой кнопке
        self.bullet_speed = 35
        self.score_multiplier = 1
        self.doublers_list = arcade.SpriteList()
        self.emitters = []
        self.last_bullet_fired = 0  # Время прошедшее с последнего выстрела
        self.bg = arcade.Sprite('pic/background.png')
        self.bg_lst = arcade.SpriteList()
        self.score_text, self.bombs_text, self.doubler_text = None, None, None
        self.score_value, self.highscore_text, self.highscore_value = None, None, None
        self.music = None
        self.points_to_achieve_bomb = 0

        self.bomb_texture = arcade.load_texture('pic/bomb.png')
        self.bomb_texture.width *= 0.4
        self.bomb_texture.height *= 0.4

        self.life_texture = arcade.load_texture('pic/game_player.png')
        self.life_texture.width *= 0.4
        self.life_texture.height *= 0.4

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()
        self.camera = True

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
        self.non_touchable_enemies_list = arcade.SpriteList()
        self.alive = True
        self.score = 0
        self.lives, self.bombs = 3, 3
        self.score_multiplier = 1
        self.activated_bombs = []
        self.doublers_list = arcade.SpriteList()
        self.emitters.clear()

        self.player = arcade.Sprite("pic/empty.png", scale=0.9)
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.sprite_list.append(self.player)

        self.emitters.append(particles.player_appearance(self.player.center_x, self.player.center_y))
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, None)
        self.move = [0, 0]
        self.fire = set()
        self.last_bullet_fired = 0

        self.stopwatch = 0  # Секундомер с начала игры (нужен и в игре, и в отладке)
        self.points_to_achieve_bomb = 1000

        arcade.schedule(self.player_spawn_particles, 0.01)
        arcade.play_sound(arcade.load_sound('sfx/player_Spawn.wav'), 0.3)
        self.music = sequence.play(0.5, loop=True)

        with open('highscores.txt') as highscores_file:
            self.file_scores = highscores_file.read().split('\n')
            for line in self.file_scores:
                level, highscore = line.split(' - ')
                if level == self.__class__.__name__:
                    self.highscore = int(highscore)

    def reset(self):
        self.stopwatch = 0
        self.alive = True
        self.enemies_list.clear()
        self.player.texture = arcade.load_texture('pic/game_player.png')
        arcade.schedule(self.player_spawn_particles, 0.01)
        arcade.play_sound(arcade.load_sound('sfx/player_Spawn.wav'), 0.3)
        self.music.play()

    def player_spawn_particles(self, *args):
        if self.stopwatch > 0.15:
            self.player.texture = arcade.load_texture('pic/game_player.png')
        if self.stopwatch <= 0.3:
            self.emitters.append(particles.player_appearance(self.player.center_x, self.player.center_y))
        if not self.emitters:
            self.enemies_generate()
            arcade.unschedule(self.player_spawn_particles)
            arcade.schedule(self.enemies_generate, 4)

    def enemies_generate(self, *args):
        n = randint(4, 15)
        for _ in range(n):
            enemy_class = choice(get_enemies())
            enemy = enemy_class()
            enemy.left = randint(0, int(SCREEN_WIDTH - enemy.width))
            enemy.bottom = randint(0, int(SCREEN_HEIGHT - enemy.height))
            self.non_touchable_enemies_list.append(enemy)

    def on_draw(self):
        self.clear()

        self.gui_camera.use()
        self.bg_lst.draw()
        for i in range(self.lives):
            arcade.draw_texture_rect(
                self.life_texture,
                arcade.rect.XYWH(self.width // 2 - (i + 0.5) * self.life_texture.width, self.height * 0.95,
                                 self.life_texture.width, self.life_texture.height)
            )
        for i in range(self.bombs):
            arcade.draw_texture_rect(
                self.bomb_texture,
                arcade.rect.XYWH(self.width // 2 + (i + 1.5) * self.bomb_texture.width, self.height * 0.95,
                                 self.bomb_texture.width, self.bomb_texture.height)
            )
        self.batch.draw()

        self.world_camera.use()
        self.sprite_list.draw()
        self.bullet_list.draw()
        self.non_touchable_enemies_list.draw()
        self.enemies_list.draw()
        self.doublers_list.draw()
        for e in self.emitters:
            e.draw()
        for x, y, radius in self.activated_bombs:
            arcade.draw_circle_outline(x, y, radius, arcade.color.WHITE, 10)
        arcade.draw_rect_outline(arcade.rect.XYWH(self.width // 2, self.height // 2, self.width, self.height),
                                 arcade.color.WHITE, border_width=5)

    def on_update(self, delta_time):
        self.stopwatch += delta_time
        particles.DELTA_TIME = delta_time
        emitters_copy = self.emitters.copy()  # Particles
        for e in emitters_copy:
            e.update(delta_time)
        for e in emitters_copy:
            if e.can_reap():
                self.emitters.remove(e)

        if not self.alive:
            self.enemies_list[0]._update(delta_time)
            if self.enemies_list[0].blinking_times == 0:
                if self.lives:
                    self.reset()
                else:
                    self.gui_camera.use()
                    game_over_view = GameOverView(self.score, self.highscore, self.__class__.__name__)
                    self.window.show_view(game_over_view)
            return

        if self.player.change_x != 0 or self.player.change_y != 0:  # Player correct angle view
            self.player.angle = math.degrees(math.atan2(self.player.change_x, self.player.change_y))

        if self.score >= self.points_to_achieve_bomb:
            self.points_to_achieve_bomb *= 10
            bomb_pickup.play()
            self.bombs += 1

        swapped = False
        for enemy in self.non_touchable_enemies_list:  # Glitching enemy (non-touchable)
            texture = enemy.texture
            enemy._update(delta_time)
            if texture != enemy.texture and enemy.texture == enemy.normal_texture:
                swapped = True
            if not enemy.is_blinking:
                enemy.remove_from_sprite_lists()
                self.enemies_list.append(enemy)
        if swapped:
            shield_off.play()

        for enemy in self.enemies_list:  # Enemy and bullet, bomb check collision
            if not enemy.is_blinking:
                enemy.move(delta_time, self.player.center_x, self.player.center_y, self.bullet_list)
            if check_for_collision_with_list(enemy, self.bullet_list):
                collided_bullets = check_for_collision_with_list(enemy, self.bullet_list)
                if collided_bullets:
                    collided_bullets[0].remove_from_sprite_lists()
                enemy.remove_from_sprite_lists()
                self.doublers_appear(enemy)
                self.score += enemy.score_per_kill * self.score_multiplier
                enemy_explode.play()
                self.emitters.append(particles.make_explosion(enemy.center_x, enemy.center_y))
            for x, y, radius in self.activated_bombs:
                distance = math.sqrt((enemy.center_x - x) ** 2 + (enemy.center_y -y) ** 2)
                if abs(distance - radius) <= 10 * 3:
                    enemy.remove_from_sprite_lists()
                    self.score += enemy.score_per_kill * self.score_multiplier
                    self.doublers_appear(enemy)

        for doubler in self.doublers_list:  # Multipliers
            doubler.move(delta_time)
            doubler._update(delta_time)

        if check_for_collision_with_list(self.player, self.doublers_list):
            picked_doublers = check_for_collision_with_list(self.player, self.doublers_list)
            self.score_multiplier += len(picked_doublers)
            for doubler in picked_doublers:
                doubler.remove_from_sprite_lists()

        for bullet in self.bullet_list:  # Bullets move
            bullet.update(delta_time)
            if (bullet.bottom > SCREEN_HEIGHT or bullet.top < 0 or
                    bullet.right < 0 or bullet.left > SCREEN_WIDTH):
                bullet.remove_from_sprite_lists()
                bullet_hitwall.play()

        self.player.change_x, self.player.change_y = self.move[0], self.move[1]  # Player move

        for i in range(len(self.activated_bombs)):  # Used bombs radius increasing
            self.activated_bombs[i][-1] += 2000 * delta_time
        self.activated_bombs = list(filter(lambda lst: lst[-1] <= self.width * 1.4142, self.activated_bombs))

        if self.fire and self.last_bullet_fired >= self.bullet_delay:  # New bullet released
            bullets = [arcade.Sprite('pic/bullet.png', 0.4) for _ in range(1)]
            for bullet in bullets:
                bullet.center_x = self.player.center_x
                bullet.center_y = self.player.center_y
            for key in self.fire:
                if key == arcade.key.UP:  # 0 1
                    bullets[0].change_y = self.bullet_speed
                elif key == arcade.key.DOWN:  # 0 -1
                    bullets[0].change_y = -self.bullet_speed
                elif key == arcade.key.LEFT:  # -1 0
                    bullets[0].change_x = -self.bullet_speed
                elif key == arcade.key.RIGHT:  # 1 0
                    bullets[0].change_x = self.bullet_speed
            for bullet in bullets:
                bullet.angle = math.degrees(math.atan2(bullet.change_x, bullet.change_y))
            self.bullet_list.extend(bullets)
            self.last_bullet_fired = 0
            fire.play(volume=0.2)

        self.last_bullet_fired += delta_time
        self.player.update(delta_time)
        # self.physics_engine.update()  # понадобится ли он? :(
        self.check_for_out_of_screen(self.player)

        if self.camera:
            target_pos = (self.player.center_x, self.player.center_y)
        else:
            target_pos = (self.width // 2, self.height // 2)
        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position, target_pos, CAMERA_SMOOTHNESS
        )

        self.highscore = max(self.highscore, self.score)

        self.score_text = arcade.Text(
            f"Score:",
            self.width * 0.01, self.height * 0.95,
            arcade.color.WHITE,
            40, align='left', anchor_x='left',
            batch=self.batch
        )

        self.score_value = arcade.Text(
            f"{self.score}",
            self.width * 0.01, self.height * 0.9,
            arcade.color.WHITE,
            40, align='left', anchor_x='left',
            batch=self.batch
        )

        self.doubler_text = arcade.Text(
            f"x{self.score_multiplier}",
            self.width // 2, self.height * 0.9,
            arcade.color.WHITE,
            32,
            batch=self.batch
        )

        self.highscore_text = arcade.Text(
            f"Highscore:",
            self.width * 0.99, self.height * 0.95,
            arcade.color.WHITE,
            40, align='right', anchor_x='right',
            batch=self.batch
        )

        self.highscore_value = arcade.Text(
            f"{self.highscore}",
            self.width * 0.99, self.height * 0.9,
            arcade.color.WHITE,
            40, align='right', anchor_x='right',
            batch=self.batch
        )

        if enemy := check_for_collision_with_list(self.player, self.enemies_list):  # Game over
            self.enemies_list.clear()
            self.non_touchable_enemies_list.clear()
            self.doublers_list.clear()
            self.bullet_list.clear()
            self.enemies_list.append(enemy[0])
            arcade.stop_sound(self.music)
            self.player.texture = arcade.load_texture('pic/empty.png')
            self.emitters.append(particles.player_explosion(self.player.center_x, self.player.center_y))
            self.lives -= 1

            enemy[0].blinking_times = 6
            enemy[0].is_blinking = True
            enemy[0].glitching_time = 0.2
            ship_explode.play()
            if self.lives == 0:
                enemy[0].blinking_times = 12
                game_over.play()
                with open('highscores.txt', 'w') as output_file:
                    for i, line in enumerate(self.file_scores):
                        level, score = line.split(' - ')
                        if level == self.__class__.__name__:
                            self.file_scores[i] = f'{level} - {self.highscore}'
                    output_file.write('\n'.join(self.file_scores))

            arcade.unschedule(self.enemies_generate)
            self.alive = False

    def check_for_out_of_screen(self, sprite: arcade.Sprite):
        if sprite.left < 0:
            sprite.left = 0
        elif sprite.right > self.width:
            sprite.right = self.width
        if sprite.bottom < 0:
            sprite.bottom = 0
        elif sprite.top > self.height:
            sprite.top = self.height

    def doublers_appear(self, enemy):
        for i in range(enemy.doublers_per_kill):
            doubler = Doubler()
            doubler.center_x = enemy.center_x
            doubler.center_y = enemy.center_y
            self.doublers_list.append(doubler)

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
        elif key == arcade.key.Q:
            if self.bombs and self.alive:
                self.activated_bombs.append([self.player.center_x, self.player.center_y, 0])
                self.bombs -= 1
                bomb_activated.play()
        elif key == arcade.key.TAB:
            self.camera = not self.camera  # По просьбе тестировщиков :)
        elif key == arcade.key.ESCAPE:
            arcade.stop_sound(self.music)
            self.gui_camera.use()
            from main_menu import MainMenuView
            self.window.show_view(MainMenuView())

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

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Geometry Wars", fullscreen=True)
    menu_view = MainMenuView()
    window.show_view(menu_view)
    arcade.run()
