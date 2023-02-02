import pygame as pg
from settings import *
from block import *

class Tetromino:
    def __init__(self, tetris, id):
        self.tetris = tetris
        self.id = id
        self.shape : list[Block] = [Block(self, pos) for pos in Tetrominos[id]]
        self.landed = False
    
    def draw(self):
        [block.draw(self.tetris.game.screen) for block in self.shape]

    def collide(self, dx=0, dy=0):
        for block in self.shape:
            if dx:
                new_x = block.pos.x + dx
                if new_x not in range(0,FIELD_WIDTH):
                    return True
                if self.tetris.field[(new_x, block.pos.y)]:
                    return True
            if dy:
                new_y = block.pos.y + dy
                if new_y >= FIELD_HEIGHT:
                    return True
                if self.tetris.field[(block.pos.x, new_y)]:
                    return True
        return False

    def move(self, dx=0, dy=0):
        if dx and (not self.collide(dx=dx)): 
            for block in self.shape:
                block.pos.x += dx

        if self.collide(dy=dy):
            self.landed = True  

        if dy and (not self.collide(dy=dy)):
            for block in self.shape:
                block.pos.y += dy
    
    def update(self):
        [block.update() for block in self.shape]