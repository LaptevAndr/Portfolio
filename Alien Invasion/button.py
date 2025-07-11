import pygame.font

class Button():
    def __init__(self, ai_settings, screen, msg):
        """Инициализирует атрибуты кнопки."""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Назначение размера и цвета кнопки
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Построение объекта rect кнопки
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Сообщение кнопки создается один раз
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Преобразует msg в изображение и центрирует его."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        """Отображает кнопку на экране."""
        # Сначала рисуем прямоугольник кнопки
        self.screen.fill(self.button_color, self.rect)
        # Затем выводим текст
        self.screen.blit(self.msg_image, self.msg_image_rect)