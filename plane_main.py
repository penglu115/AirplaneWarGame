import pygame
from plane_sprites import *
from menu_button import *


class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self):
        self.life_times = LIFE_TIMES
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.__create_sprite()
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)
        pygame.time.set_timer(ENEMY_FIRE_EVENT, 1000)

    def __create_sprite(self):
        # 背景
        bg1 = Background(False)
        bg2 = Background(True)
        self.bg_group = pygame.sprite.Group(bg1, bg2)

        # 生命值
        self.life_group = pygame.sprite.Group()

        self.enemy_group = pygame.sprite.Group()
        self.enemy_bullet_group = pygame.sprite.Group()
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

        start_button = StartMenu()
        finish_button = FinishMenu()
        self.button_group = pygame.sprite.Group(start_button, finish_button)

    def start_game(self):
        self.life_times = LIFE_TIMES
        for num in range(1, self.life_times+1):
            life = Life(num)
            self.life_group.add(life)

        while True:
            self.clock.tick(FRAME_PER_SEC)  # 设置刷新帧率
            self.__event_handler(True)  # 事件监听
            self.__check_collide()  # 碰撞检测
            self.__update_sprites(True)  # 更新/绘制精灵组
            pygame.display.update()  # 更新显示

    def menu(self):
        while True:
            self.clock.tick(FRAME_PER_SEC)  # 设置刷新帧率
            self.__event_handler(False)  # 事件监听
            self.__update_sprites(False)  # 更新/绘制精灵组
            pygame.display.update()  # 更新显示

    def __event_handler(self, isgame):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__finish()
            elif event.type == CREATE_ENEMY_EVENT and isgame:
                enemy = Enemy()
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT and isgame:
                self.hero.fire()
            elif event.type == ENEMY_FIRE_EVENT and isgame:
                for enemy in self.enemy_group:
                    bullets = enemy.fire()
                    for bullet in bullets:
                        self.enemy_bullet_group.add(bullet)
            elif event.type == pygame.MOUSEBUTTONDOWN and isgame is False:
                get_pos = pygame.mouse.get_pos()
                for button in self.button_group:
                    if button.isClick(get_pos):
                        if button.name == 'start':
                            self.start_game()
                        if button.name == 'finish':
                            self.__finish()
        if isgame:
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_RIGHT]:
                self.hero.speed = 1
            elif key_pressed[pygame.K_LEFT]:
                self.hero.speed = -1
        else:
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_UP]:
                self.start_game()
            elif key_pressed[pygame.K_DOWN]:
                self.__finish()

    def __check_collide(self):
        # 敌机碰撞子弹
        enemy_list1 = pygame.sprite.groupcollide(self.enemy_group, self.hero.bullet_group, False, True)
        for enemy in enemy_list1:
            enemy.collided = True

        # hero碰撞敌机
        enemy_list2 = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if len(enemy_list2) != 0:
            self.hero.collided = True
            for enemy in enemy_list2:
                enemy.collided = True

        # hero碰撞敌机子弹
        bullets = pygame.sprite.spritecollide(self.hero, self.enemy_bullet_group, True)
        if len(bullets) != 0:
            self.hero.collided = True

        if self.hero.collided_time > 60:
            self.__game_over()

    def __update_sprites(self, isgame):
        self.bg_group.update()
        self.bg_group.draw(self.screen)
        if isgame:
            self.life_group.update()
            self.life_group.draw(self.screen)
            self.enemy_group.update()
            self.enemy_group.draw(self.screen)
            self.enemy_bullet_group.update()
            self.enemy_bullet_group.draw(self.screen)
            self.hero_group.update()
            self.hero_group.draw(self.screen)
            self.hero.bullet_group.update()
            self.hero.bullet_group.draw(self.screen)
        else:
            self.button_group.draw(self.screen)

    def __game_over(self):
        for life in self.life_group:
            if life.life_num == self.life_times:
                self.life_group.remove(life)
                life.kill()
        self.hero.collided = False
        self.hero.collided_time = 0
        self.life_times -= 1

        if self.life_times <= 0:
            for enemy in self.enemy_group:
                enemy.kill()
            for bullet in self.enemy_bullet_group:
                bullet.kill()
            for bullet in self.hero.bullet_group:
                bullet.kill()
            self.menu()

    @staticmethod
    def __finish():
        pygame.quit()
        exit()


if __name__ == '__main__':
    game = PlaneGame()
    game.menu()
