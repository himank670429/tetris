import pygame as pg
from tetris import *
from settings import *

class Game():
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        self.main_game = MainGame(self)

    def run(self):
        self.new()
        while self.running:
            self.dt = self.clock.tick(FPS)
            self.event()
            self.draw()
            self.update()
    
    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN: self.main_game.move_tetromino(event.key)

    def draw(self):
        self.screen.fill((0,0,0))
        self.main_game.draw()
    
    def update(self):
        self.main_game.update()
        pg.display.update()

if __name__ == "__main__":
    game = Game()
    while True:
        game.run()