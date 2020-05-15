import pygame
from plane_sprites import SCREEN_RECT


class ButtonSprite(pygame.sprite.Sprite):

    def __init__(self, image_name):
        super().__init__()
        self.name = 'button'
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()

    def update(self):
        pass

    def isClick(self, pos):
        if (self.rect.left <= pos[0] <= self.rect.right
                and self.rect.top <= pos[1] <= self.rect.bottom):
            return True
        else:
            return False


class StartMenu(ButtonSprite):
    def __init__(self):
        super().__init__('./images/again.png')
        self.name = 'start'
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 200


class FinishMenu(ButtonSprite):
    def __init__(self):
        super().__init__('./images/gameover.png')
        self.name = 'finish'
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120
