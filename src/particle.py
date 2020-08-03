import pygame
from constant import *
import drawing


class Particle(pygame.sprite.Sprite):
    """
    Class that represents a particle

    Attributes:
        x (arg, int): x position of particle
        y (arg, int): y position of particle
        v_x (int): x velocity of particle
        v_y (int): y velocity of particle
        max_x (int): max x position of particle (after which it disappears)
        max_y (int): max y position of particle (after which it disappears)
        group (arg, Group): group particle belongs to
    """
    # TODO: add check for when actual map is smaller than RESOLUTION,
    #       so x and y aren't in sync just like the mouse cursor
    def __init__(self, x, y, group):
        pygame.sprite.Sprite.__init__(self)
        self.x = x * SPRITE_SIZE
        self.y = y * SPRITE_SIZE
        self.v_x = 2
        self.v_y = -6
        self.max_x = self.x
        self.max_y = self.y
        self.image = pygame.Surface((8, 8))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.group = group

    def update(self):
        self.rect.topleft = (self.x, self.y)
        self.x += self.v_x
        self.y += self.v_y
        self.v_y += 0.5
        if self.y >= self.max_y:
            self.group.remove(self)
