import arcade
import math
from main_menu import MainMenuView

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()


class GameOverView(arcade.View):
    def __init__(self, score, highscore, level_name):
        super().__init__()
        self.score = score
        self.highscore = highscore
        self.level_name = level_name
        self.background_lst = arcade.SpriteList()
        self.selected_item = 0
        self.menu_items = ["ИГРАТЬ СНОВА", "ГЛАВНОЕ МЕНЮ"]
        self.title_color = arcade.color.RED_DEVIL
        self.color_cycle = 0
        self.gui_camera = None
        self.background = arcade.Sprite("pic/GameOver.png")

    def on_show_view(self):
        self.gui_camera = arcade.camera.Camera2D()
        self.background_lst = arcade.SpriteList()

        self.background.width = SCREEN_WIDTH
        self.background.height = SCREEN_HEIGHT
        self.background.center_x = SCREEN_WIDTH // 2
        self.background.center_y = SCREEN_HEIGHT // 2
        self.background_lst.append(self.background)

    def on_draw(self):
        self.clear()
        self.gui_camera.use()

        self.background_lst.draw()

        for offset in [(-6, -6), (6, -6), (-6, 6), (6, 6), (0, -6), (0, 6), (-6, 0), (6, 0)]:
            arcade.draw_text(
                "GAME OVER",
                SCREEN_WIDTH // 2 + offset[0],
                SCREEN_HEIGHT * 0.75 + offset[1],
                (0, 0, 0, 200),
                100,
                anchor_x="center",
                anchor_y="center",
                bold=True,
                font_name="Kenney Future"
            )

        arcade.draw_text(
            "GAME OVER",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT * 0.75,
            self.title_color,
            100,
            anchor_x="center",
            anchor_y="center",
            bold=True,
            font_name="Kenney Future"
        )

        formatted_score = f"{self.score:,}".replace(",", " ")
        formatted_highscore = f"{self.highscore:,}".replace(",", " ")

        for offset in [(-3, -3), (3, -3), (-3, 3), (3, 3)]:
            arcade.draw_text(
                "ВАШ СЧЕТ",
                SCREEN_WIDTH // 2 + offset[0],
                SCREEN_HEIGHT * 0.55 + offset[1],
                (0, 0, 0, 200),
                40,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )

        arcade.draw_text(
            "ВАШ СЧЕТ",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT * 0.55,
            arcade.color.WHITE,
            40,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        score_color = arcade.color.GOLD if self.score >= self.highscore else arcade.color.WHITE
        for offset in [(-4, -4), (4, -4), (-4, 4), (4, 4), (0, -4), (0, 4)]:
            arcade.draw_text(
                f"{formatted_score}",
                SCREEN_WIDTH // 2 + offset[0],
                SCREEN_HEIGHT * 0.48 + offset[1],
                (0, 0, 0, 200),
                60,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )

        arcade.draw_text(
            f"{formatted_score}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT * 0.48,
            score_color,
            60,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        for offset in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
            arcade.draw_text(
                "РЕКОРД",
                SCREEN_WIDTH // 2 + offset[0],
                SCREEN_HEIGHT * 0.38 + offset[1],
                (0, 0, 0, 200),
                30,
                anchor_x="center",
                anchor_y="center"
            )

        arcade.draw_text(
            "РЕКОРД",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT * 0.38,
            arcade.color.WHITE,
            30,
            anchor_x="center",
            anchor_y="center"
        )

        for offset in [(-3, -3), (3, -3), (-3, 3), (3, 3)]:
            arcade.draw_text(
                f"{formatted_highscore}",
                SCREEN_WIDTH // 2 + offset[0],
                SCREEN_HEIGHT * 0.33 + offset[1],
                (0, 0, 0, 200),
                40,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )

        arcade.draw_text(
            f"{formatted_highscore}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT * 0.33,
            arcade.color.GOLD,
            40,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        if self.score >= self.highscore and self.score > 0:
            for offset in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
                arcade.draw_text(
                    "НОВЫЙ РЕКОРД!",
                    SCREEN_WIDTH // 2 + offset[0],
                    SCREEN_HEIGHT * 0.28 + offset[1],
                    (0, 0, 0, 200),
                    30,
                    anchor_x="center",
                    anchor_y="center",
                    bold=True
                )

            arcade.draw_text(
                "НОВЫЙ РЕКОРД!",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT * 0.28,
                arcade.color.ELECTRIC_GREEN,
                30,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )

        for i, item in enumerate(self.menu_items):
            color = arcade.color.ELECTRIC_YELLOW if i == self.selected_item else arcade.color.WHITE

            for offset in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
                arcade.draw_text(
                    item,
                    SCREEN_WIDTH // 2 + offset[0],
                    SCREEN_HEIGHT * 0.18 - i * 60 + offset[1],
                    (0, 0, 0, 200),
                    40,
                    anchor_x="center",
                    anchor_y="center",
                    bold=(i == self.selected_item)
                )

            arcade.draw_text(
                item,
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT * 0.18 - i * 60,
                color,
                40,
                anchor_x="center",
                anchor_y="center",
                bold=(i == self.selected_item)
            )

        for offset in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
            arcade.draw_text(
                "ENTER - выбрать    ESC - главное меню",
                SCREEN_WIDTH // 2 + offset[0],
                SCREEN_HEIGHT * 0.05 + offset[1],
                (0, 0, 0, 150),
                20,
                anchor_x="center",
                anchor_y="center"
            )

        arcade.draw_text(
            "ENTER - выбрать    ESC - главное меню",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT * 0.05,
            arcade.color.LIGHT_GRAY,
            20,
            anchor_x="center",
            anchor_y="center"
        )

    def on_update(self, delta_time):
        self.color_cycle += delta_time * 2
        color_value = 150 + int(105 * (1 + math.sin(self.color_cycle)) / 2)
        self.title_color = (255, color_value, color_value)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.selected_item = (self.selected_item - 1) % len(self.menu_items)
        elif key == arcade.key.DOWN:
            self.selected_item = (self.selected_item + 1) % len(self.menu_items)
        elif key == arcade.key.ENTER or key == arcade.key.SPACE:
            if self.selected_item == 0:
                if self.level_name == 'Evolved':
                    from main import Evolved
                    game_view = Evolved()
                    game_view.setup()
                    self.window.show_view(game_view)
                elif self.level_name == 'Deadline':
                    from main import Deadline
                    game_view = Deadline()
                    game_view.setup()
                    self.window.show_view(game_view)
            elif self.selected_item == 1:
                self.window.show_view(MainMenuView())
        elif key == arcade.key.ESCAPE:
            self.window.show_view(MainMenuView())