class Settings():
    """Класс для хранения всех настроек игры Alien Invasion."""
    
    def __init__(self):
        """Инициализирует статические настройки игры."""
        # Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)  # Серый цвет фона
        
        # Настройки корабля
        self.ship_speed_factor = 1.5     # Скорость перемещения корабля
        
        # Параметры пуль
        self.bullet_speed_factor = 3      # Скорость пули
        self.bullet_width = 3             # Ширина пули
        self.bullet_height = 15           # Высота пули
        self.bullet_color = (60, 60, 60)  # Темно-серый цвет пуль
        self.bullets_allowed = 3          # Максимальное количество пуль

        # Настройки пришельцев
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10        # Скорость движения флота
        self.fleet_direction = 1          # Направление движения флота вправо ( -1 влево )

        self.ship_limit = 3  # Количество жизней/попыток

        # Темп ускорения игры 
        self.speedup_scale = 1.1
        # Темп роста стоимости пришельцев
        self.score_scale = 1.5
        self.initialize_dymanic_settings()

    def initialize_dymanic_settings(self):
        """Инициализирует настройки, зависящие от уровня."""
        self.ship_speed_factor = 1.5 
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.fleet_direction = 1

        # Подсчет очков
        self.alien_points = 50
    
    def increase_speed(self):
        """Увеличивает настройки скорости."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
