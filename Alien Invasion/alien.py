import pygame
import os
from pygame.sprite import Sprite

class Alien(Sprite):
    """Класс, представляющий 1 пришельца"""
    def __init__(self, ai_settings, screen):
        """Инициализирует пришельца и задает его начальную позицию"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #Загрузка изображения пришельца и назначение атрибута rect
        current_dir = os.path.dirname(__file__)
        image_path = os.path.join(current_dir, 'images', 'alien.bmp')
        self.image = pygame.image.load(image_path)

        self.rect = self.image.get_rect()

        # Каждый новый пришелец появляется в левом верхнем углу экрана.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение точной позиции пришельца.
        self.x = float(self.rect.x)
    
    def blitme(self):
        """Рисует пришельца в текущей позиции"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Проверяет, достиг ли пришелец края экрана"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Перемещает пришельза вправо или влево"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
