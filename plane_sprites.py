import random
import pygame

# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# life图片大小
PLANE_LIFE_RECT = pygame.Rect(0, 0, 46, 57)
# 刷新的帧率
FRAME_PER_SEC = 60
# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# hero发射子弹定时器
HERO_FIRE_EVENT = pygame.USEREVENT + 1
# enemy发射子弹定时器
ENEMY_FIRE_EVENT = pygame.USEREVENT + 2
# 最大命数
LIFE_TIMES = 3


class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self, image_name, speed):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        self.rect.y += self.speed


class Background(GameSprite):
    """游戏背景精灵"""
    def __init__(self, is_alt=False, speed=1):
        super().__init__('./images/background.png', speed)
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.y


class Life(GameSprite):
    def __init__(self, life_num):
        super().__init__('./images/life.png', 0)
        self.rect.right = PLANE_LIFE_RECT.width * life_num
        self.rect.y = 0
        self.life_num = life_num

    def update(self):
        pass


class Enemy(GameSprite):
    def __init__(self):
        speed = random.randint(1, 3)
        self.image_name = './images/enemy%d.png' % (random.randint(1, 2))
        super().__init__(self.image_name, speed)
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)
        self.rect.bottom = 0
        self.collided = False
        self.collided_time = 0

    def update(self):
        if self.collided:
            if self.collided_time >= 60:
                self.kill()
                return
            else:
                down_name = '.' + self.image_name.split('.')[1] + '_down' + str((self.collided_time//15+1)) + '.png'
                self.image = pygame.image.load(down_name)
            self.collided_time += 1
        else:
            super().update()
            if self.rect.y >= SCREEN_RECT.height:
                self.kill()

    def fire(self):
        bullets = []
        num_bullet = 1
        for n in range(1, num_bullet+1):
            bullet = Bullet('./images/bullet2.png', self.speed + 1)
            bullet.rect.top = self.rect.bottom + 20 * n
            bullet.rect.centerx = self.rect.centerx
            bullets.append(bullet)
        return bullets


class Hero(GameSprite):
    def __init__(self, speed=0):
        super().__init__('./images/me1.png', speed)
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120
        self.bullet_group = pygame.sprite.Group()
        self.collided = False
        self.collided_time = 0

    def update(self):
        if self.collided:
            if self.collided_time >= 60:
                self.image = pygame.image.load("./images/me1.png")
            else:
                self.image = pygame.image.load("./images/me_destroy_%d.png" % (self.collided_time//15+1))
            self.collided_time += 1
        else:
            self.rect.x += self.speed
            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > SCREEN_RECT.width:
                self.rect.right = SCREEN_RECT.width

    def fire(self):
        num_bullet = 3
        for n in range(1, num_bullet+1):
            bullet = Bullet('./images/bullet1.png', -2)
            bullet.rect.bottom = self.rect.top + 20 * n
            bullet.rect.centerx = self.rect.centerx
            self.bullet_group.add(bullet)


class Bullet(GameSprite):
    def __init__(self, image_name, speed=-2):
        super().__init__(image_name, speed)

    def update(self):
        super().update()
        if self.rect.bottom <= 0:
            self.kill()


if __name__ == '__main__':
    pass
