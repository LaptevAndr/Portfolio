import sys
import pygame
from bullet import Bullet

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """
    Реагирует на нажатие клавиш.
    Параметры:
        event: объект события pygame
        ai_settings: объект настроек игры
        screen: объект экрана игры
        ship: объект корабля игрока
        bullets: группа пуль
    """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # Создание новой пули и добавление в группу bullets
        if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    """
    Реагирует на отпускание клавиш.
    Параметры:
        event: объект события pygame
        ship: объект корабля игрока
    """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, ship, bullets):
    """
    Обрабатывает нажатия клавиш и события мыши.
    Параметры:
        ai_settings: объект настроек игры
        screen: объект экрана игры
        ship: объект корабля игрока
        bullets: группа пуль
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def update_bullets(bullets):
    """
    Обновляет позиции пуль и удаляет старые пули.
    Параметры:
        bullets: группа пуль
    """
    # Обновление позиций пуль
    bullets.update()
    
    # Удаление пуль, вышедших за край экрана
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

def update_screen(ai_settings, screen, ship, bullets, alien):
    """
    Обновляет изображения на экране и отображает новый экран.
    Параметры:
        ai_settings: объект настроек игры
        screen: объект экрана игры
        ship: объект корабля игрока
        bullets: группа пуль
    """
    # Перерисовка экрана при каждом проходе цикла
    screen.fill(ai_settings.bg_color)
    
    # Все пули выводятся позади корабля и пришельцев
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    # Отрисовка корабля и пришельцев
    ship.blitme()
    alien.blitme()

    # Отображение последнего прорисованного экрана
    pygame.display.flip()