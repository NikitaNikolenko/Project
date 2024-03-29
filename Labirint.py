from pygame import *


# Зробимо батьківський клас для усіх спрайтів у грі
class GameSprite(sprite.Sprite):
    # Конструктор класу
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()  # викликаємо конструктор батьківського класу
        # Завантаження та зміна розміру зображення
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed  # Швидкість спрайту
        self.rect = self.image.get_rect()  # Отримання прямокутника, обведеного навколо зображення
        self.rect.x = player_x  # Початкова позиція по осі Х
        self.rect.y = player_y  # Початкова позиція по осі Y

    # Метод для відображення спрайту на екрані
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# Створимо дочірній клас для спрайту-гравця
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_w - 80:
            self.rect.x += self.speed
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_DOWN] and self.rect.y < win_h - 80:
            self.rect.y += self.speed


# Клас(д) для спрайта ворога(переміщається сам)
class Enemy(GameSprite):
    direction = "left"

    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= win_w - 85:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_w, wall_h):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_w
        self.height = wall_h
        self.image = Surface((self.width, self.height))  # Створює об'єкт Surface заднаої ширини та висоти
        self.image.fill((color_1, color_2, color_3))  # Заповнює об'єкт кольором(RGB)
        # Кожен спрайт повинен зберігати властивість rect - прямокутник
        self.rect = self.image.get_rect()  # Визначає прямокуну область,яку займає спрайт
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))  # Розміщуємо зображення стіни
        # Намалювати прямокутник


# Розмір вікна гри
win_w = 700
win_h = 500
# Створення  вікна гри
window = display.set_mode((win_w, win_h))
display.set_caption("Лабіринт")  # Заголовок вікна
# Завантажили та змінили розмір фону
background = transform.scale(image.load("background.jpg"), (win_w, win_h))

# Створимо об'єкт гравця, монстра та скарбу
player = Player("hero.png", 5, win_h - 80, 4)
monster = Enemy("cyborg.png", win_w - 80, 280, 2)
final = GameSprite("treasure.png", win_w - 120, win_h - 80, 0)

# Стіни
w1 = Wall(99, 135, 130, 100, 170, 10, 270)
w2 = Wall(99, 135, 130, 70, 430, 450, 10)
w3 = Wall(99, 135, 130, 400,250, 400, 10)
w4 = Wall(99, 135, 130, 400, 200, 450, 10)
w5 = Wall(99, 135, 130, 250, 170, 450, 10)

game = True
finish = False
clock = time.Clock()
FPS = 60
font.init()
font = font.Font(None,70)
win = font.render("YOU WIN",True,(255,215,0))
lose = font.render("YOU LOSE",True,(180,0,0))
# Інізіалізація музичного модуля та відтворення муз файлу
mixer.init()
mixer.music.load("jungles.ogg")
mixer.music.play()
kick = mixer.Sound("kick.ogg")
money = mixer.Sound("money.ogg")

time = 0

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        window.blit(background, (0, 0))
        player.update()
        monster.update()

        player.reset()
        monster.reset()
        final.reset()

        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
    if sprite.collide_rect(player,w1) or sprite.collide_rect(player,monster) or sprite.collide_rect(player,w2) or sprite.collide_rect(player,w3):
        finish = True
        window.blit(lose,(200,200))
        kick.play()
        time += clock.tick(FPS)
        if time == 100:
            finish = False
            player.rect.x = 5
            player.rect.y = win_h - 80
            time = 0

    display.update()
    clock.tick(FPS)