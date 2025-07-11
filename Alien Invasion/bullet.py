import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Класс для управления пулями, выпущенными кораблем."""
    def __init__(self, ai_settings, screen, ship):
        """Создает объект пули в текущей позиции корабля."""
        super().__init__()
        self.screen = screen
        
        # Создание пули в позиции (0,0) и назначение правильной позиции
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, 
                               ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        # Позиция пули хранится в вещественном формате
        self.y = float(self.rect.y)
        
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Перемещает пулю вверх по экрану."""
        # Обновление позиции пули в вещественном формате
        self.y -= self.speed_factor
        # Обновление позиции прямоугольника
        self.rect.y = self.y

    def draw_bullet(self):
        """Выводит пулю на экран."""
        pygame.draw.rect(self.screen, self.color, self.rect)
    
    def draw_button(self):
        """Выводит кнопку на экран."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)