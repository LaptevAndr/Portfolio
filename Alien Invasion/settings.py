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
        self.bullet_speed_factor = 2      # Скорость пули
        self.bullet_width = 3             # Ширина пули
        self.bullet_height = 15           # Высота пули
        self.bullet_color = (60, 60, 60)  # Темно-серый цвет пуль
        self.bullets_allowed = 3          # Максимальное количество пуль

        # Настройки пришельцев
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10        # Скорость движения флота
        self.fleet_direction = 1          # Направление движения флота вправо ( -1 влево )
