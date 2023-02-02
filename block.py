from settings import *
import pygame as pg

vec = pg.math.Vector2
class Block:
    def __init__(self, tetromino, pos):
        self.tetromino = tetromino
        self.pos = vec(pos)
        self.image = pg.Surface((TILE, TILE))
        self.image.fill((255,29,20))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.topleft = self.pos * TILE

    def draw(self, surface):
        surface.blit(self.image, self.rect)
