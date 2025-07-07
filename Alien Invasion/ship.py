import pygame
import os
from pygame.sprite import Sprite

class Ship(Sprite):
    """Класс для управления кораблем игрока."""
    def __init__(self, ai_settings, screen):
        """
        Инициализирует корабль и задает его начальную позицию.
        """
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        # Загрузка изображения корабля и получение его прямоугольника
        current_dir = os.path.dirname(__file__)  # Получаем директорию текущего файла
        image_path = os.path.join(current_dir, 'images', 'ship.bmp')
        self.image = pygame.image.load(image_path)
        
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        # Каждый новый корабль появляется у нижнего края экрана по центру
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # Сохранение вещественной координаты центра корабля
        self.center = float(self.rect.centerx)
        
        # Флаги перемещения
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """
        Обновляет позицию корабля с учетом флагов перемещения.
        Ограничивает перемещение в пределах экрана.
        """
        # Обновление атрибута center, не rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
            
        # Обновление rect на основании self.center
        self.rect.centerx = self.center

    def blitme(self):
        """Рисует корабль в текущей позиции."""
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        """Сбрасывает корабль в центр экрана."""
        self.center = self.screen_rect.centerx