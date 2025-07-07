import pygame.font
import os
from pygame.sprite import Sprite, Group
from ship import Ship

class Heart(Sprite):
    """Класс для изображения сердца"""
    def __init__(self, ai_settings, screen):
        super(Heart, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        current_dir = os.path.dirname(__file__)
        image_path = os.path.join(current_dir, 'images', 'heart.bmp')
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

class Scoreboard():
    """Класс для вывода счета игрока"""
    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Настройки шрифта для вывода счета
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Подготовка исходного изображения
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_hearts()

    def prep_score(self):
        """Преобразует текущий счет в изображение"""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)
        # Вывод счета в правом верхнем углу экрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Преобразует лучший счет в изображение"""
        high_score = int(round(self.stats.score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)
        # Рекорд выравнивается по центру в верхней части экрана
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top


    def show_score(self):
        """Вывод счета на экран"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # Вывод оставшихся жизней.
        self.hearts.draw(self.screen)
    
    def prep_level(self):
        """Преобразует текущий уровень в изображение"""
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)
        # Уровень выводится под текущим счетом
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
    
    def prep_hearts(self):
        """Преобразует количество жизней в сердечки"""
        self.hearts = Group()
        for heart_number in range(self.stats.ships_left):
            heart = Heart(self.ai_settings, self.screen)
            heart.rect.x = 10 + heart_number * (heart.rect.width + 10)
            heart.rect.y = 40
            self.hearts.add(heart)