import sys
import pygame
from bullet import Bullet
from alien import Alien

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

def update_bullets(aliens, bullets):
    """
    Обновляет позиции пуль и удаляет старые пули.
    """
    # Обновление позиций пуль
    bullets.update()
    
    # Удаление пуль, вышедших за край экрана
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    # Проверка попаданий в пришельцев.
    # При обнаружении попадания удаляем пришельца и пулю.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

def update_screen(ai_settings, screen, ship, bullets, aliens):
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
    aliens.draw(screen)

    # Отображение последнего прорисованного экрана
    pygame.display.flip()

def get_number_aliens_x(ai_settings, alien_width):
    """Вычисляет количество пришельцев в ряду."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """Вычисляет количество рядов пришельцев"""
    available_space_y = (ai_settings.screen_height - 
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Создает пришельца и размещает его в ряду."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Создает флот пришельцев."""
    # Создание пришельца и вычисление количества пришельцев в ряду.
    alien = Alien(ai_settings, screen)

    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Создание флота пришельцев.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """Проверяет, достиг ли флот края экрана."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Опускает весь флот и меняет направление флота."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings, aliens):
    """Проверяет, достиг ли флот края экрана,
        после чего обновляет позиции всех пришельцев во флоте."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()