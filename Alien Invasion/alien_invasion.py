import pygame
from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf 

def run_game():
    """Инициализирует игру, настройки и создает экран.
    Запускает главный игровой цикл.
    """
    # Инициализация pygame, настроек и объекта экрана
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    # Создание корабля и группы для хранения пуль
    ship = Ship(ai_settings, screen)
    bullets = pygame.sprite.Group()
    
    # Создание пришельца.
    alien = Alien(ai_settings, screen)

    # Запуск основного цикла игры
    while True:
        # Отслеживание событий клавиатуры и мыши
        gf.check_events(ai_settings, screen, ship, bullets)
        # Обновление позиции корабля
        ship.update()
        # Обновление позиций пуль
        gf.update_bullets(bullets)
        # Обновление изображений на экране
        gf.update_screen(ai_settings, screen, ship, bullets, alien)

run_game() 