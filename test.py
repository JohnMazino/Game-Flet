import flet as ft
import random
import threading
import time
import pygame

def spaceship_game(page: ft.Page):
    # Настройка размеров окна
    page.window.width = 1280
    page.window.height = 720
    page.bgcolor = ft.Colors.BLACK
    
    # Инициализация звуков
    #pygame.mixer.init()
    #pygame.mixer.music.load("\\background_music.mp3")  # Фоновая музыка
    #pygame.mixer.music.set_volume(0.5)
    #pygame.mixer.music.play(-1)  # Повторять музыку бесконечно
    #shoot_sound = pygame.mixer.Sound("\\shoot.wav")  # Звук выстрела
    #shoot_sound.set_volume(0.5)
    #collision_sound = pygame.mixer.Sound("\\collision.wav")  # Звук столкновения
    #collision_sound.set_volume(0.5)
    
    # Создание корабля
    spaceship = ft.Image(
        src=f"\\pon.jpg",
        width=50,
        height=50,
        top=335,  # Центрирование по вертикали
        left=615,   # Центрирование по горизонтали
    )
    
    # Создание астероидов
    asteroids = []
    asteroid_images = [
        f"\\op.jpg"
    ]
    # Начальное количество астероидов
    initial_asteroid_count = 4
    
    # Функция для создания астероидов
    def create_asteroids():
        nonlocal asteroids
        asteroids = []
        for i in range(initial_asteroid_count):
            asteroid = ft.Image(
                src=asteroid_images[i % len(asteroid_images)],  # Используем циклический выбор изображений(должно было быть больше космического мусора)
                width=30,
                height=30,
                top=random.randint(-100, -30),  # Начинают появляться сверху
                left=random.randint(0, 1250)
            )
            asteroids.append(asteroid)
    
    create_asteroids()
    
    # Переменная для скорости астероидов и корабля
    speed = 15  
    
    # Переменная для счетчика очков
    score = 0
    # Обновление счетчика очков
    score_label = ft.Text(value=f"Очки: {score}", color=ft.Colors.WHITE, size=20)
    score_label.top = 10
    score_label.left = 10
    
    # Функция для ускорения игры
    def increase_speed():
        nonlocal speed
        while not stop_threads:
            time.sleep(5)  # Увеличиваем скорость каждые 5 секунд
            speed += 1
            print(f"Скорость увеличена до {speed}")
    
    # Обработка событий клавиатуры для перемещения корабля и стрельбы
    def on_keyboard(e: ft.KeyboardEvent):
        nonlocal speed, can_shoot
        step = speed  # Шаг перемещения зависит от текущей скорости
        if e.key == "w" or e.key == "W":
            spaceship.top = max(spaceship.top - step, 0)
        elif e.key == "s" or e.key == "S":
            spaceship.top = min(spaceship.top + step, 670)
        elif e.key == "a" or e.key == "A":
            spaceship.left = max(spaceship.left - step, 0)
        elif e.key == "d" or e.key == "D":
            spaceship.left = min(spaceship.left + step, 1230)
        elif e.key == " " and can_shoot:  # Стрельба при нажатии пробела
            can_shoot = False
            bullet = ft.Image(
                src=f"\\i.jpg",  # Изображение пули
                width=10,
                height=20,
                top=spaceship.top - 10,  # Позиция пули над кораблем
                left=spaceship.left + 20  # Позиция пули по центру корабля
            )
            bullets.append(bullet)
            #shoot_sound.play()
            game_area.controls.append(bullet)
            page.update()
            # Перезарядка
            threading.Thread(target=reload).start()
            page.update()
    
    def reload():
        nonlocal can_shoot
        time.sleep(1)  # Время перезарядки
        can_shoot = True
    
    # Проверка столкновений
    def check_collision(obj1, obj2):
        obj1_left = obj1.left
        obj1_top = obj1.top
        obj1_right = obj1_left + obj1.width
        obj1_bottom = obj1_top + obj1.height
        obj2_left = obj2.left
        obj2_top = obj2.top
        obj2_right = obj2_left + obj2.width
        obj2_bottom = obj2_top + obj2.height
        return (obj1_left < obj2_right and
                obj1_right > obj2_left and
                obj1_top < obj2_bottom and
                obj1_bottom > obj2_top)
    
    def check_collisions():
        nonlocal score
        while not stop_threads:
            for asteroid in asteroids[:]:
                if check_collision(spaceship, asteroid):
                    #collision_sound.play()
                    snack_bar = ft.SnackBar(content=ft.Text("Столкновение!"))
                    page.overlay.append(snack_bar)
                    snack_bar.open = True
                    page.update()
                    # Останавливаем игру
                    stop_game()
                    return
            for bullet in bullets[:]:
                for asteroid in asteroids[:]:
                    if check_collision(bullet, asteroid):
                        bullets.remove(bullet)
                        game_area.controls.remove(bullet)
                        asteroids.remove(asteroid)
                        game_area.controls.remove(asteroid)
                        score += 100
                        score_label.value = f"Очки: {score}"
                        page.update()
            time.sleep(0.05)
    
    # Функция для добавления новых астероидов
    def add_asteroids():
        current_asteroid_count = initial_asteroid_count
        while not stop_threads:
            if current_asteroid_count < 10:  # Максимальное количество астероидов
                time.sleep(10)  # Добавляем новый астероид каждые 10 секунд
                asteroid = ft.Image(
                    src=asteroid_images[current_asteroid_count % len(asteroid_images)],  # Используем циклический выбор изображений
                    width=30,
                    height=30,
                    top=random.randint(-100, -30),  # Начинают появляться сверху
                    left=random.randint(0, 1250)
                )
                asteroids.append(asteroid)
                game_area.controls.append(asteroid)
                current_asteroid_count += 1
                print(f"Добавлен новый астероид. Общее количество: {current_asteroid_count}")
            else:
                break
    
    # Функция для создания белых полос
    def create_white_strips():
        strips = []
        for i in range(10):
            strip = ft.Container(
                bgcolor=ft.Colors.WHITE,
                width=random.randint(1, 2),  # Случайная ширина полосы
                height=25,  # Высота полосы
                top=random.randint(-100, -30),  # Начинают появляться сверху
                left=random.randint(0, 1275)  # Случайное положение по горизонтали
            )
            strips.append(strip)
        return strips
    
    # Создание белых полос
    white_strips = create_white_strips()
    
    # Функция для движения белых полос
    def move_white_strips():
        while not stop_threads:
            for strip in white_strips:
                strip.top += speed  # Двигаемся вниз
                if strip.top > 720:  # Если полоса уходит за экран
                    strip.top = random.randint(-100, -30)  # Возвращаем сверху
                    strip.left = random.randint(0, 1275)  # Новое случайное положение по горизонтали
                    strip.width = random.randint(1, 2)  # Новая случайная ширина полосы
            page.update()
            time.sleep(0.01)  # Уменьшаем задержку для более плавного движения полос
    
    # Функция для начисления очков каждую секунду
    def increase_score():
        nonlocal score
        while not stop_threads:
            time.sleep(0.5)  # Начисляем очки каждую секунду(теперь пол)
            score += 1
            score_label.value = f"Очки: {score}"
            page.update()
    
    # Функция для обновления всех элементов игры
    def update_game_elements():
        threading.Thread(target=move_asteroids).start()
        threading.Thread(target=move_bullets).start()
        threading.Thread(target=move_white_strips).start()
        threading.Thread(target=check_collisions).start()
        threading.Thread(target=add_asteroids).start()
        threading.Thread(target=increase_speed).start()
        threading.Thread(target=increase_score).start()
    
    # Обновление позиции астероидов
    def move_asteroids():
        nonlocal speed
        while not stop_threads:
            for asteroid in asteroids:
                asteroid.top += speed  # Двигаемся вниз
                if asteroid.top > 750:  # Если астероид уходит за экран
                    asteroid.top = random.randint(-100, -30)
                    asteroid.left = random.randint(0, 1250)
            page.update()
            time.sleep(0.05)
    
    # Список для хранения пуль
    bullets = []
    
    # Функция для движения пуль
    def move_bullets():
        while not stop_threads:
            for bullet in bullets[:]:
                bullet.top -= speed  # Пули двигаются быстрее астероидов(теперь нет)
                if bullet.top < -10:  # Если пуля уходит за экран
                    bullets.remove(bullet)
                    game_area.controls.remove(bullet)
            page.update()
            time.sleep(0.01)  # Уменьшаем задержку для более плавного движения пуль
    
    # Функция для начала игры
    def start_game(e):
        nonlocal score, can_shoot, asteroids, bullets, speed
        score = 0
        score_label.value = f"Очки: {score}"
        page.update()
        
        # Сброс астероидов
        for asteroid in asteroids:
            game_area.controls.remove(asteroid)
        create_asteroids()
        for asteroid in asteroids:
            game_area.controls.append(asteroid)
        
        # Сброс пуль
        for bullet in bullets:
            game_area.controls.remove(bullet)
        bullets.clear()
        
        # Сброс скорости
        speed = 15
        
        # Сброс корабля
        spaceship.top = 335
        spaceship.left = 615
        
        page.on_keyboard_event = on_keyboard
        update_game_elements()  # Запуск всех потоков игры
        start_button.visible = False
        can_shoot = True  # Разрешаем стрельбу
        page.update()
    
    # Функция для завершения игры
    def stop_game():
        nonlocal stop_threads
        stop_threads = True
        page.on_keyboard_event = None
        start_button.visible = True
        page.update()
        # Ждем завершения всех потоков
        time.sleep(1)
        stop_threads = False
    
    # Создание кнопки "Начать игру"
    start_button = ft.ElevatedButton(
        text="Начать игру",
        on_click=start_game,
        width=200,
        height=50,
        top=335,
        left=540
    )
    
    # Создание стека для размещения корабля, астероидов, белых полос и кнопки
    game_area = ft.Stack(
        [
            spaceship,
            score_label,
            start_button,
            *asteroids,  # Распаковываем список астероидов
            *white_strips  # Распаковываем список белых полос
        ],
        width=1280,
        height=720
    )
    
    # Добавление игрового поля на страницу
    page.clean()
    page.add(game_area)
    
    # Переменная для остановки потоков
    stop_threads = False
    
    # Переменная для контроля перезарядки оружия
    can_shoot = True
    
    # Обработчик закрытия приложения
    def on_close(e):
        nonlocal stop_threads
        stop_threads = True
        pygame.mixer.music.stop()
        page.update()
    
    # Назначение обработчика закрытия окна
    page.window.on_close = on_close

# нельзя нажимать кнопку сразу после поражения, иначе потоки не успевают запуститься, 
# полноэкранный режим плохо работает, а в окне не видно четких границ карты

# Для запуска игры
ft.app(target=spaceship_game, assets_dir="image")