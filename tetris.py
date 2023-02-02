from settings import *
from tetromino import *
import pygame as pg
from random import choice
class MainGame:
    def __init__(self, game):
        self.game = game
        self.field = {}
        for x in range(FIELD_WIDTH):
            for y in range(FIELD_HEIGHT):
                self.field[(x,y)] = False
        self.tetromino = Tetromino(self, choice(list(Tetrominos.keys())))
        self.start = pg.time.get_ticks()
        self.now = pg.time.get_ticks()  
    
    def update(self):
        if self.now - self.start > horizontal_delay:
            self.tetromino.move(dy=1)
            self.start = self.now
        self.now = pg.time.get_ticks()
        self.tetromino.update()
        if self.tetromino.landed:
            self.new_tetromino()
    
    def new_tetromino(self):
        # registering landed shapes
        for block in self.tetromino.shape:
            x,y = block.pos
            self.field[(x,y)] = True
        self.tetromino = Tetromino(self, choice(list(Tetrominos.keys())))
        

    def move_tetromino(self, key):
        if key == pg.K_LEFT: self.tetromino.move(dx=-1)
        elif key == pg.K_RIGHT: self.tetromino.move(dx=1)
    

    def draw(self):
        # draw landed tetromino
        for point in self.field:
            if self.field[point]:
                # draw static tetromino
                pg.draw.rect(self.game.screen, (255,255,255) ,pg.Rect(point[0]*TILE, point[1]*TILE, TILE, TILE))
        self.tetromino.draw()
