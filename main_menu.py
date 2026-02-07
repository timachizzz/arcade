import arcade

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


class MainMenuView(arcade.View):
    """Класс для главного меню"""

    def __init__(self):
        super().__init__()
        self.background = None
        self.menu_items = ["НАЧАТЬ ИГРУ", "НАСТРОЙКИ", "ВЫХОД"]
        self.selected_item = 0
        self.menu_font_size = 50
        self.title_font_size = 100
        self.background_lst = arcade.SpriteList()

    def on_show_view(self):
        self.background = arcade.Sprite("pic/background.png")
        # Растягиваем фон на весь экран
        self.background.width = SCREEN_WIDTH
        self.background.height = SCREEN_HEIGHT
        self.background.center_x = SCREEN_WIDTH // 2
        self.background.center_y = SCREEN_HEIGHT // 2
        self.background_lst.append(self.background)

        # Если текстура не найдена, создается простой фон
        if not self.background.texture:
            print("Фоновая текстура menu_background.png не найдена! Используется цветной фон.")
            arcade.set_background_color(arcade.color.COOL_BLACK)
    def on_draw(self):
        self.clear()
        self.background_lst.draw()
        arcade.draw_text("Geometry Wars",
                         SCREEN_WIDTH // 2,
                         SCREEN_HEIGHT * 0.75,
                         arcade.color.WHITE,
                         self.title_font_size,
                         anchor_x="center",
                         anchor_y="center",
                         bold=True)

        for i, item in enumerate(self.menu_items):
            color = arcade.color.GOLD if i == self.selected_item else arcade.color.WHITE
            arcade.draw_text(item,
                             SCREEN_WIDTH // 2,
                             SCREEN_HEIGHT * 0.5 - i * 70,
                             color,
                             self.menu_font_size,
                             anchor_x="center",
                             anchor_y="center",
                             bold=(i == self.selected_item))

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.selected_item = (self.selected_item - 1) % len(self.menu_items)
        elif key == arcade.key.DOWN:
            self.selected_item = (self.selected_item + 1) % len(self.menu_items)
        elif key == arcade.key.ENTER or key == arcade.key.SPACE:
            if self.selected_item == 0:
                # Запуск игры
                from main import GameView
                game_view = GameView()
                game_view.setup()
                self.window.show_view(game_view)
            elif self.selected_item == 1:
                # Переход к настройкам
                settings_view = SettingsView(self)
                self.window.show_view(settings_view)
            elif self.selected_item == 2:
                # Выход из игры
                arcade.close_window()
        elif key == arcade.key.ESCAPE:
            arcade.close_window()


class SettingsView(arcade.View):
    """Класс для экрана настроек"""
    def __init__(self, main_menu):
        super().__init__()
        self.main_menu = main_menu
        self.selected_setting = 0
        self.fullscreen = False
        self.settings = [
            f"ПОЛНЫЙ ЭКРАН: {'ВКЛ' if self.fullscreen else 'ВЫКЛ'}",
            "НАЗАД"
        ]

    def on_draw(self):
        """Отрисовка настроек"""
        self.clear()

        arcade.draw_text("НАСТРОЙКИ",
                         SCREEN_WIDTH // 2,
                         SCREEN_HEIGHT * 0.8,
                         arcade.color.WHITE,
                         70,
                         anchor_x="center",
                         anchor_y="center",
                         bold=True)

        self.settings[0] = f"ПОЛНЫЙ ЭКРАН: {'ВКЛ' if self.fullscreen else 'ВЫКЛ'}"

        for i, setting in enumerate(self.settings):
            color = arcade.color.GOLD if i == self.selected_setting else arcade.color.WHITE
            arcade.draw_text(setting,
                             SCREEN_WIDTH // 2,
                             SCREEN_HEIGHT * 0.6 - i * 80,
                             color,
                             40,
                             anchor_x="center",
                             anchor_y="center",
                             bold=(i == self.selected_setting))

    def on_key_press(self, key, modifiers):
        """Обработка нажатий клавиш"""
        if key == arcade.key.UP:
            self.selected_setting = (self.selected_setting - 1) % len(self.settings)
        elif key == arcade.key.DOWN:
            self.selected_setting = (self.selected_setting + 1) % len(self.settings)
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            if self.selected_setting == 0:
                self.fullscreen = not self.fullscreen
                self.window.set_fullscreen(self.fullscreen)
        elif key == arcade.key.ENTER:
            if self.selected_setting == 1:
                self.window.show_view(self.main_menu)
        elif key == arcade.key.ESCAPE:
            self.window.show_view(self.main_menu)

