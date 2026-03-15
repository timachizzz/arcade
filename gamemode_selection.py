import arcade

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()


class ModeSelectView(arcade.View):
    """Экран выбора режима игры"""

    def __init__(self, main_menu):
        super().__init__()
        self.main_menu = main_menu
        self.background = None
        self.background_lst = arcade.SpriteList()
        self.selected_mode = 0
        self.gui_camera = None

        # Загрузка текстур для режимов
        self.evolved_texture = arcade.load_texture("pic/game_player.png")

        # Рекорд для первого режима
        self.highscore = 0
        self.load_highscore()

    def load_highscore(self):
        """Загружает рекорд для режима Evolved"""
        try:
            with open('highscores.txt', 'r') as file:
                lines = file.read().split('\n')
                for line in lines:
                    if ' - ' in line:
                        level, score = line.split(' - ')
                        if level == "Evolved":
                            self.highscore = int(score)
        except (FileNotFoundError, ValueError):
            self.highscore = 0

    def on_show_view(self):
        """Вызывается при открытии экрана"""
        self.gui_camera = arcade.camera.Camera2D()

        # Настройка фона
        self.background = arcade.Sprite("pic/background.png")
        self.background.width = SCREEN_WIDTH
        self.background.height = SCREEN_HEIGHT
        self.background.center_x = SCREEN_WIDTH // 2
        self.background.center_y = SCREEN_HEIGHT // 2
        self.background_lst = arcade.SpriteList()
        self.background_lst.append(self.background)

    def on_draw(self):
        """Отрисовка экрана выбора режима"""
        self.clear()
        self.gui_camera.use()
        self.background_lst.draw()

        arcade.draw_lbwh_rectangle_filled(
            0, SCREEN_WIDTH, SCREEN_HEIGHT, 0,
            (0, 0, 0, 150)
        )

        arcade.draw_text(
            "ВЫБЕРИТЕ РЕЖИМ",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT * 0.85,
            arcade.color.WHITE,
            80,
            anchor_x="center",
            anchor_y="center",
            bold=True,
            font_name="Kenney Future"
        )

        self.draw_mode_1()

        self.draw_mode_2()

        arcade.draw_text(
            "←/→ - выбрать    ENTER - играть    ESC - назад",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT * 0.1,
            arcade.color.LIGHT_GRAY,
            20,
            anchor_x="center",
            anchor_y="center"
        )

    def draw_mode_1(self):
        """Отрисовка первого режима (Evolved)"""
        x_center = SCREEN_WIDTH // 2 - 300
        y_center = SCREEN_HEIGHT // 2
        width = 500
        height = 300

        left = x_center - width // 2
        bottom = y_center - height // 2

        if self.selected_mode == 0:
            arcade.draw_lbwh_rectangle_outline(
                left, bottom, width, height,
                arcade.color.ELECTRIC_BLUE, 4
            )
            # Заливка с прозрачностью
            arcade.draw_lbwh_rectangle_filled(
                left, bottom, width, height,
                (arcade.color.ELECTRIC_BLUE[0],
                 arcade.color.ELECTRIC_BLUE[1],
                 arcade.color.ELECTRIC_BLUE[2], 30)
            )

        # Основная обводка
        arcade.draw_lbwh_rectangle_outline(
            left, bottom, width, height,
            arcade.color.WHITE, 2
        )

        texture_width = self.evolved_texture.width * 1.5
        texture_height = self.evolved_texture.height * 1.5
        texture_left = x_center - 150 - texture_width // 2
        texture_bottom = y_center + 50 - texture_height // 2
        texture_right = texture_left + texture_width
        texture_top = texture_bottom + texture_height

        arcade.draw_texture_rect(
            texture=self.evolved_texture,
            rect=arcade.Rect(
                left=texture_left,
                right=texture_right,
                bottom=texture_bottom,
                top=texture_top,
                width=texture_width,
                height=texture_height,
                x=texture_left + texture_width // 2,
                y=texture_bottom + texture_height // 2
            )
        )

        # Название режима
        arcade.draw_text(
            "EVOLVED",
            x_center + 50, y_center + 80,
            arcade.color.ELECTRIC_BLUE,
            36,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        # Описание
        arcade.draw_text(
            "Классический режим",
            x_center + 50, y_center + 30,
            arcade.color.LIGHT_GRAY,
            14,
            anchor_x="center",
            anchor_y="center",
            align="center"
        )

        arcade.draw_text(
            "Противники появляются постепенно",
            x_center + 50, y_center + 5,
            arcade.color.LIGHT_GRAY,
            12,
            anchor_x="center",
            anchor_y="center",
            align="center"
        )

        arcade.draw_text(
            "3 жизни, 3 бомбы",
            x_center + 50, y_center - 20,
            arcade.color.LIGHT_GRAY,
            14,
            anchor_x="center",
            anchor_y="center",
            align="center",
            bold=True
        )

        # Рекорд
        formatted_highscore = f"{self.highscore:,}".replace(",", " ")
        arcade.draw_text(
            f"🏆 {formatted_highscore}",
            x_center + 50, y_center - 70,
            arcade.color.GOLD if self.highscore > 0 else arcade.color.LIGHT_GRAY,
            18,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

    def draw_mode_2(self):
        """Отрисовка второго режима (Coming Soon)"""
        x_center = SCREEN_WIDTH // 2 + 300
        y_center = SCREEN_HEIGHT // 2
        width = 500
        height = 300

        left = x_center - width // 2
        bottom = y_center - height // 2

        # Подсветка выбранного режима
        if self.selected_mode == 1:
            arcade.draw_lbwh_rectangle_outline(
                left, bottom, width, height,
                arcade.color.LIGHT_GRAY, 4
            )
            arcade.draw_lbwh_rectangle_filled(
                left, bottom, width, height,
                (100, 100, 100, 50)
            )

        arcade.draw_lbwh_rectangle_filled(
            left, bottom, width, height,
            (30, 30, 30, 200)
        )

        arcade.draw_lbwh_rectangle_outline(
            left, bottom, width, height,
            arcade.color.DARK_GRAY, 2
        )

        # Текст "COMING SOON" по диагонали
        arcade.draw_text(
            "COMING",
            x_center - 30, y_center + 40,
            arcade.color.GRAY,
            40,
            rotation=-15,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        arcade.draw_text(
            "SOON",
            x_center + 30, y_center - 20,
            arcade.color.GRAY,
            48,
            rotation=-15,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        # Текст с описанием
        arcade.draw_text(
            "НОВЫЙ РЕЖИМ",
            x_center, y_center - 80,
            arcade.color.LIGHT_GRAY,
            18,
            anchor_x="center",
            anchor_y="center",
            align="center",
            bold=True
        )

        arcade.draw_text(
            "СКОРО",
            x_center, y_center - 110,
            arcade.color.LIGHT_GRAY,
            22,
            anchor_x="center",
            anchor_y="center",
            align="center",
            bold=True
        )

    def on_key_press(self, key, modifiers):
        """Обработка нажатий клавиш"""
        if key == arcade.key.LEFT:
            self.selected_mode = 0
        elif key == arcade.key.RIGHT:
            self.selected_mode = 1
        elif key == arcade.key.ENTER:
            if self.selected_mode == 0:
                # Локальный импорт здесь
                from main import Evolved
                game_view = Evolved()
                game_view.setup()
                self.window.show_view(game_view)
        elif key == arcade.key.ESCAPE:
            self.window.show_view(self.main_menu)