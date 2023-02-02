# game constants
FIELD_WIDTH = 10
FIELD_HEIGHT = 20
TILE = 32
SCREEN_WIDTH = FIELD_WIDTH * TILE
SCREEN_HEIGHT = FIELD_HEIGHT * TILE
FPS = 60

# ticks (time interval)
horizontal_delay = 500

# tetromino
Tetrominos = {
    1:[(0,0),(0,1),(0,2),(0,3)],
    2:[(0,0),(0,1),(1,0),(1,1)],
    3:[(0,0),(0,1),(0,2),(1,1)],
    4:[(1,0),(1,1),(0,1),(0,2)],
    5:[(0,0),(0,1),(0,2),(1,2)],
    6:[(0,0),(0,1),(1,1),(1,2)],
    7:[(1,0),(1,1),(1,2),(0,2)]
}
