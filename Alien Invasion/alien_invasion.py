import pygame
from pygame.sprite import Group
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
    bullets = Group()
    aliens = Group()
    
    # Создание флота пришельцев.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Запуск основного цикла игры
    while True:
        # Отслеживание событий клавиатуры и мыши
        gf.check_events(ai_settings, screen, ship, bullets)
        # Обновление позиции корабля
        ship.update()
        # Обновление позиций пуль
        gf.update_bullets(aliens, bullets)
        # Обновление позиций пришельцев
        gf.update_aliens(ai_settings, aliens)
        # Обновление изображений на экране
        gf.update_screen(ai_settings, screen, ship, bullets, aliens)


run_game() 