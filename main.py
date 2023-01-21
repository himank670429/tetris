from pygame import *
from random import randint
from os import path,listdir
from pickle import load,dump
from time import sleep

# initialize
init()
font.init()
mixer.init()

vec = math.Vector2
shape = 0
nextshape = 0
nextshapeindex = 0
nextshapesize = (50,50)
HorizontalTicks = 0
VerticalTicks = 0
VerticalTickIncrementConstant = 20
BaseVerticalsTicks = 600
LineCheckConstant = 30
previouslines = 0
accelarating = False
W = 10
H = 20
_W = 200
_H = 100
Tile = 32
border = 40 
paused = False
bgcolor = (34,33,52)
textColor = (200,200,200)
fontSize = 40

# level
Level = 1
level_up_message_tick = 5000

UIoffset = 100
screen_width = W * Tile + UIoffset + (border*2)
screen_height = H * Tile + (border*2)
gameOver = False
gameOverDuration = 4000
shapeAppeared = False

score_pop_up_pos = (0,0)
score_pop_up_ticks = 0
score_pop_up_delay = 300
is_score_poping_out = False

# scores
lines = 0
highscore = 0
score = 0
highscore_beaten = False

current_music = None

screen = display.set_mode((screen_width, screen_height))

area = {}
for x in range(W):
    for y in range(H):
        area[(x,y)] = 0

# folder and file paths
fileFolder = path.dirname(__file__)
AssetsFolder = path.join(fileFolder,"Assets")
spritesFolder = path.join(AssetsFolder,"sprites")
animationFolder = path.join(AssetsFolder,"animation_sprites")
tileFolder = path.join(spritesFolder,"tile")
backgroundFolder = path.join(spritesFolder,"background")
FontFolder = path.join(AssetsFolder,"fonts")
GUIfolder = path.join(spritesFolder,"GUI")
soundfolder = path.join(AssetsFolder,"sound")
datafile = "tetris.dat"

if not path.exists(path.join(fileFolder,datafile)):
    with open(path.join(fileFolder,datafile),"wb") as file:
        dump(0,file)

# images loading
# background 
bgImage = image.load(path.join(backgroundFolder,"BackGround.png"))
bgImage = transform.scale(bgImage,(screen_width, screen_height))
MainMenuImage = image.load(path.join(backgroundFolder,"MainMenu.png"))
MainMenuImage = transform.scale(MainMenuImage,(screen_width,screen_height))
EmptyBackground = image.load(path.join(backgroundFolder,"EmptyBackground.png"))
EmptyBackground = transform.scale(EmptyBackground,(screen_width,screen_height))

# tiles 
redTile = image.load(path.join(tileFolder,"red.png"))
brownTile = image.load(path.join(tileFolder,"brown.png"))
blueTile = image.load(path.join(tileFolder,"blue.png"))
pinkTile = image.load(path.join(tileFolder,"pink.png"))
orangeTile = image.load(path.join(tileFolder,"orange.png"))
cyanTile = image.load(path.join(tileFolder,"cyan.png"))
greenTile = image.load(path.join(tileFolder,"green.png"))
whiteTile = image.load(path.join(tileFolder,"white.png"))

# GUI
messageboxImage = transform.scale(image.load(path.join(GUIfolder,"messagebox.png")),(_W,_H))
trophy = transform.scale(image.load(path.join(GUIfolder, "trophy.png")), (50,50))


# font loading
gameFont = path.join(FontFolder,"gameFont.ttf")

# animation sprites
animations = {
    types : [
        image.load(f'{animationFolder}//{types}//{frame}')
        for frame in listdir(f'{animationFolder}//{types}')
    ] 
    for types in listdir(animationFolder)
}

dance_animations = ["dancer_leg_hand", "dancer_flips"]

# musics
troika = path.join(soundfolder,"Torika.mp3")
brandinsky = path.join(soundfolder,"Brandinsky.mp3")
loginska = path.join(soundfolder,"Loginska.mp3")
karinka = path.join(soundfolder,"Karinka.mp3")
level_up = path.join(soundfolder,"Level Up.mp3")
level_clear = path.join(soundfolder,"Level clear.mp3")
title = path.join(soundfolder,"title theme.mp3")
game_over = path.join(soundfolder,"Game Over.mp3")
dancer_dance = path.join(soundfolder, "dancer dance.mp3")

# SFX
score_clear = mixer.Sound(path.join(soundfolder,"Level clear.mp3"))
tetromino_placed = mixer.Sound(path.join(soundfolder, "tetromino placed.mp3"))
line_cleared = mixer.Sound(path.join(soundfolder, "line clear.mp3"))
dancer_cry = line_cleared

TileSprites = {
    1:{"shape":[(0,0),(0,1),(0,2),(0,3)],"tile":redTile},
    2:{"shape":[(0,0),(0,1),(1,0),(1,1)],"tile":blueTile},
    3:{"shape":[(0,0),(0,1),(0,2),(1,1)],"tile":brownTile},
    4:{"shape":[(1,0),(1,1),(0,1),(0,2)],"tile":cyanTile},
    5:{"shape":[(0,0),(0,1),(0,2),(1,2)],"tile":pinkTile},
    6:{"shape":[(0,0),(0,1),(1,1),(1,2)],"tile":greenTile},
    7:{"shape":[(1,0),(1,1),(1,2),(0,2)],"tile":orangeTile}
}
nextshapes = {
    1 : transform.scale2x(image.load(path.join(GUIfolder, 'straight line.png'))),
    2 : transform.scale2x(image.load(path.join(GUIfolder, 'O.png'))),
    3 : transform.scale2x(image.load(path.join(GUIfolder, 'T.png'))),
    4 : transform.scale2x(image.load(path.join(GUIfolder, 'cyan Z.png'))),
    5 : transform.scale2x(image.load(path.join(GUIfolder, 'pink L.png'))),
    6 : transform.scale2x(image.load(path.join(GUIfolder, 'green Z.png'))),
    7 : transform.scale2x(image.load(path.join(GUIfolder, 'orange L.png')))
}

# initialize the staitic tiles with white colors
StaticTileColors = [whiteTile,redTile,brownTile,blueTile,orangeTile,pinkTile,cyanTile,greenTile]
StaticTileindex = 0
StaticTileImage = StaticTileColors[StaticTileindex]

# classes
class Scene:
    MainMenu = 1
    AudioSelect = 2
    RunGame = 3
    EndGame = 4

scene = Scene.MainMenu

class button():
    def __init__(self,x,y,text,fontSize,fonttype,color,textalign = "center"):
        self.textfont = font.Font(fonttype,fontSize)
        self.textsurf = self.textfont.render(text,True,color,None)
        self.textrect = self.textsurf.get_rect()
        if textalign == "topleft": self.textrect.topleft = (x,y)
        elif textalign == "topright": self.textrect.topright = (x,y)
        elif textalign == "center": self.textrect.center = (x,y)
        elif textalign == "bottomleft": self.textrect.bottomleft = (x,y)
        elif textalign == "bottomright": self.textrect.bottomright = (x,y)
        self.width = self.textrect.width
        self.height = self.textrect.height
    def isCMousePointerCollide(self):
        return self.textrect.collidepoint(mouse.get_pos())
    def render(self):
        screen.blit(self.textsurf,self.textrect)

class AnimatedSprite:
    def __init__(self,animation_sprites, pos, fps = 4, align = "center", size = None):
        self.frames = animation_sprites
        self.pos = pos
        self.current_frame_index = 0
        self.start = self.now = time.get_ticks()
        self.align = align
        self.size = size
        self.fps = fps
        if self.size:
            sprite_pos = None
            if self.align == "center":
                sprite_pos = (
                    self.pos[0] - (size[0]/2),
                    self.pos[1] - (size[1]/2)
                )

            elif self.align == "topleft":
                sprite_pos = (
                    self.pos[0],
                    self.pos[1]
                )

            elif self.align == "top":
                sprite_pos = (
                    self.pos[0] - (size[0]/2),
                    self.pos[1]
                )

            elif self.align == "topright":
                sprite_pos = (
                    self.pos[0] - (size[0]),
                    self.pos[1]
                )

            elif self.align == "bottomleft":
                sprite_pos = (
                    self.pos[0],
                    self.pos[1] - (size[1])
                )

            elif self.align == "bottom":
                sprite_pos = (
                    self.pos[0] - (size[0]/2),
                    self.pos[1] - (size[1])
                )
            
            elif self.align == "bottomright":
                sprite_pos = (
                    self.pos[0] - (size[0]),
                    self.pos[1] - (size[1])

                )
            
            elif self.align == "right":
                sprite_pos = (
                    self.pos[0] - (size[0]),
                    self.pos[1] - (size[1]/2)
                )
            
            elif self.align == "left":
                sprite_pos = (
                    self.pos[0],
                    self.pos[1] - (size[1]/2)
                )
            self.pos = sprite_pos

    def get_pos(self):
        return self.pos
    
    def set_pos(self, newpos):
        self.pos = newpos
    
    def set_animation_frames(self, newframe):
        self.frames = newframe
        self.current_frame_index = 0

    def animate(self, sound=None, frame = 1):
        global screen
        current_frame = self.frames[self.current_frame_index]
        if self.size: current_frame = transform.scale(current_frame, self.size)
        screen.blit(current_frame, (self.pos))
        if self.now - self.start > (1/self.fps)*1000:
            self.current_frame_index += 1
            self.current_frame_index %= len(self.frames)
            self.start = self.now
            if sound and self.current_frame_index == frame: sound.play()
        self.now = time.get_ticks()

def newshape(index):
    shape = {
        "points" : [],
        "tile":None,
    }
    tileshape = TileSprites[index]["shape"]
    shape["tile"] = TileSprites[index]["tile"]
    offset = 4
    for point in tileshape:
        x = point[0]+offset
        y = point[1]
        shape["points"].append(vec(x,y))
    return shape

def collide(shape_,deltax = 0,deltay = 0):
    for point in shape_:
        x1 = point.x
        y1 = point.y
        x2 = int(x1 + deltax)
        y2 = int(y1 + deltay)
        if deltax == -1:
            if (x2<0) or (area[(x2,y1)]):
                return True
        if deltax == 1:
            if (x2>=W) or (area[(x2,y1)]):
                return True

        # detect vertical collision
        if (y2 >= H) or (area[(x1,int(y2))]):
            return True
    return False

def registerStaticShape(shape_):
    for point in shape_:
        x = point.x
        y = point.y
        area[(x,y)] = True

def updatestaticshape(row_y):
    for y in range(int(row_y),-1,-1):
        for x in range(W):
            if not y==0:
                area[(x,y)] = area[(x,y-1)]

def checkrow(shape):
    global lines, accelarating, score, highscore
    row_appeared = 0
    lines_appeared = 0
    y = max([point.y for point in shape])
    for dy in range(4):
        _y = y - dy
        if _y < 0:
            return
        while isRowAppear(_y):
            # for _x in range(W):
            #     area[(_x,_y)] = False
            # delete row
            global nextshape
            # animation
            _x = 0
            now = start = time.get_ticks()
            while _x < W:
                display.update()
                screen.blit(bgImage,(0,0))
                drawText(screen,(415,120),textColor,gameFont,20,f'{lines}',align="center")  # lines
                drawText(screen,(415,220),textColor,gameFont,20,f'{highscore}',align="center")  # high score
                drawText(screen,(415,295),textColor,gameFont,20,f'{score}',align="center")  # score
                drawText(screen,(415,500),textColor,gameFont,20,f'{Level}',align="center") # level
                for Event in event.get():
                    if Event.type == QUIT:
                        quit()
                        exit()
                if now - start > 10:
                    area[(_x,_y)] = False
                    _x += 1
                    start = now
                now = time.get_ticks()
                # static shape draw
                for point in area:
                    x = point[0]
                    y = point[1]
                    if (area[(int(x),int(y))]):
                        screen.blit(StaticTileImage,(x*Tile + border,y*Tile + border))
                # nextshape draw
                screen.blit(nextshape,(screen_width-100,screen_height/2+10))
            
            row_appeared = 1
            lines_appeared += 1
            lines += 1
            updatestaticshape(_y)
    if row_appeared :
        line_cleared.play()        
        accelarating = 0
    if lines_appeared == 1:
        score += (40*(Level-1))
    if lines_appeared == 2:
        score += (100*(Level-1))
    if lines_appeared == 3:
        score += (300*(Level-1))
    if lines_appeared == 4:
        score += (1200*(Level-1))

def isRowAppear(y):
    for x in range(W):
        if not area[(x,y)]:
            return False
    return True

def spaceToRotate(shape_):
    center = shape_[1]
    for point in shape_:
        x1 = int(center.x - point.x)
        y1 = int(center.y - point.y)
        x2 = center.x + y1
        y2 = center.y - x1
        if (x2<0) or (x2>=W) or (y2<0) or (y2>=H):
            return True
        if area[(x2,y2)]:
            return True
    return False

def spaceToSpawn(shape):
    for point in shape:
        x = point.x
        y = point.y
        if area[(x,y)]:
            return False
    return True

def drawText(surface,pos,color,_font,size,text,align="topleft"):
    textFont = font.Font(_font,size)
    textSurf = textFont.render(text,True,color,None)
    textRect = textSurf.get_rect()
    if align == "topleft":textRect.topleft = pos
    elif align == "topright":textRect.topright = pos
    elif align == "center":textRect.center = pos
    elif align == "bottomleft":textRect.bottomleft = pos
    elif align == "bottomright":textRect.bottomright = pos
    surface.blit(textSurf,textRect)

def displaymessage(text):
    global messageboxImage
    screen.blit(messageboxImage,((((W*Tile)/2 + border - (_W/2)),(screen_height/2)-(_H/2))))
    messageboxRect = messageboxImage.get_rect()
    messageboxRect.topleft = ((((W*Tile)/2 + border - (_W/2)),(screen_height/2)-(_H/2)))
    drawText(screen,messageboxRect.center,(255,255,255),gameFont,30,text,align="center")

def game_over_animation():
    mixer.music.load(game_over)
    # do gameover stuff
    start = time.get_ticks()
    now = time.get_ticks()
    mixer.music.play()
    while (now-start < gameOverDuration):
        displaymessage("gameOver")
        display.update()
        for Event in event.get():
            if Event.type == QUIT:
                # close high score before quiting
                with open(path.join(fileFolder,datafile),"wb") as file:
                    dump(max(score,highscore),file)
                exit()
            if Event.type == KEYDOWN:
                if Event.key == K_SPACE or Event.key == K_RETURN:
                    mixer.music.unload()

                    return
        now = time.get_ticks()

def dancer_animation():
    mixer.music.load(dancer_dance)
    mixer.music.play()
    walkin_speed = .17
    start = now = time.get_ticks()
    animation_state = "coming"
    # coming
    # dancing
    dance_animation_index = randint(0,1)
    dancer = AnimatedSprite(animations['dancer_walks_right'],(border+60, screen_height-border),align="bottom", size = (100,100), fps = 7)

    while True:
        screen.blit(bgImage,(0,0))
        drawText(screen,(415,120),textColor,gameFont,20,f'{lines}',align="center")  # lines
        drawText(screen,(415,220),textColor,gameFont,20,f'{highscore}',align="center")  # high score
        drawText(screen,(415,295),textColor,gameFont,20,f'{score}',align="center")  # score
        drawText(screen,(415,500),textColor,gameFont,20,f'{Level}',align="center") # level
    
        if animation_state == "coming":
            dancer_pos = dancer.get_pos()
            dancer.set_pos((dancer_pos[0] + walkin_speed, dancer_pos[1]))
        
        if dancer.get_pos()[0] >= (screen_width/2 - border*2) and animation_state == "coming":
            animation_state = "dancing"
            dancer.set_animation_frames(animations[dance_animations[dance_animation_index]])
            
        if animation_state == "dancing":
            if now - start > 2600:
                start = now
                dance_animation_index += 1
                dance_animation_index %= len(dance_animations)
                dancer.set_animation_frames(animations[dance_animations[dance_animation_index]])
            now = time.get_ticks()

        if animation_state == "idle":
            if now - start > 1200:
                animation_state = "returning"
                dancer.set_animation_frames(animations['dancer_walks_left'])
            now = time.get_ticks()
        
        if animation_state == "returning":
            dancer_pos = dancer.get_pos()
            dancer.set_pos((dancer_pos[0] - walkin_speed, dancer_pos[1]))

        if dancer.get_pos()[0] < (border*3 - 60) and animation_state == "returning":
            return

        if not mixer.music.get_busy():
            if animation_state == "dancing":
                dancer.set_animation_frames(animations["dancer_idle"])
                animation_state = "idle"
                now = start = time.get_ticks()
                start = now = time.get_ticks()
            mixer.music.unload()
        for Event in event.get():
            if Event.type == QUIT:
                # close high score before quiting
                with open(path.join(fileFolder,datafile),"wb") as file:
                    dump(max(score,highscore),file)
                exit()
            if Event.type == KEYDOWN:
                mixer.music.unload()
                return
        dancer.animate()
        display.update()



def level_up_animation():
    flag = 1
    global level_up_animation_tick,accelarating
    start = time.get_ticks()
    now = time.get_ticks()
    mixer.music.load(level_up)
    mixer.music.play()
    while (now-start < level_up_message_tick) and flag:
        screen.blit(bgImage,(0,0))
        drawText(screen,(415,120),textColor,gameFont,20,f'{lines}',align="center")  # lines
        drawText(screen,(415,220),textColor,gameFont,20,f'{highscore}',align="center")  # high score
        drawText(screen,(415,295),textColor,gameFont,20,f'{score}',align="center")  # score
        drawText(screen,(415,500),textColor,gameFont,20,f'{Level}',align="center") # level
        displaymessage("level up")
        for Event in event.get():
            if Event.type == QUIT:
                # close high score before quiting
                with open(path.join(fileFolder,datafile),"wb") as file:
                    dump(max(score,highscore),file)
                quit()
                exit()
            if Event.type == KEYDOWN:
                flag = 0
        display.update()
        now = time.get_ticks()
    dancer_animation()

# loading stuff
with open(path.join(fileFolder,datafile),"rb") as file:
    highscore = load(file)


# scenes
def EndGame():
    start = now = time.get_ticks()
    global scene, highscore_beaten, score, highscore
    # initialize the dancer
    click = False
    dancer = None
    flag = 1
    text1 = text2 = None
    if (highscore_beaten):
        score_clear.play()
        dancer = AnimatedSprite(animations["dancer_jumps"], (screen_width/2-110, 200), align="center", size = (100,100))
        text1 = "congractulations! you are"
        text2 = "the best player yet!!"
    else:
        dancer = AnimatedSprite(animations["dancer_cry"], (screen_width/2-110, 200), align="center", size = (100,100)) 
        text1 = "you couldn't beat"   
        text2 = "the high score!!"
    exit_button = button(screen_width/2, screen_height/2+200,"main menu",30,gameFont,textColor)
    # run the loop
    while flag:
        screen.blit(EmptyBackground, (0,0))
        # do the animation stuff
        dancer.animate(sound = dancer_cry, frame = 1)
        if (highscore_beaten):
            screen.blit(trophy, (115, 80))
        drawText(screen, (screen_width/2+70, 170), textColor, gameFont, 30, f"your score : {score}", align="center")
        drawText(screen, (screen_width/2+70, 220), textColor, gameFont, 30, f"highsocre : {highscore}", align="center")
        drawText(screen, (screen_width/2, screen_height/2), textColor, gameFont, 30, text1, align="center")
        drawText(screen, (screen_width/2, screen_height/2+40), textColor, gameFont, 30, text2, align="center")
        exit_button.render()
        click = False
        display.update()
        for Event in event.get():
            if Event.type == QUIT:
                # close high score before quiting
                with open(path.join(fileFolder,datafile),"wb") as file:
                    dump(max(score,highscore),file)
                exit()
            if Event.type == MOUSEBUTTONDOWN: click = True
            if exit_button.isCMousePointerCollide() and click: flag = 0
        if now - start > 10000:
            flag = 0
        now = time.get_ticks()

    # after it gets out of while loop
    screen.blit(EmptyBackground,(0,0))
    display.update()
    sleep(1)
    scene = Scene.MainMenu
    if highscore_beaten:
        highscore = score
        score = 0
        highscore_beaten = False
    # saving high score
    with open(path.join(fileFolder,datafile),"wb") as file:
        dump(max(score,highscore),file)
    score_clear.stop()


def RunGame():
    global HorizontalTicks,VerticalTicks,shapeAppeared,score,gameOver,paused,shape,nextshape,nextshapeindex,accelarating,Level,lines,previouslines,LineCheckConstant,score,highscore,StaticTileImage,StaticTileColors,StaticTileindex,current_music, scene, highscore_beaten
    if current_music != "None":
        mixer.music.load(current_music)
        mixer.music.play(-1)
    lines = 0
    # Variables
    while True:
        rotate = False
        dx = 0
        verticalDelay = BaseVerticalsTicks - ((Level-1) * VerticalTickIncrementConstant)
        horizontalDelay = 120
        # event checking
        for Event in event.get():

            if Event.type == QUIT:
                # close high score before quiting
                with open(path.join(fileFolder,datafile),"wb") as file:
                    dump(max(score,highscore),file)
                exit()
            if Event.type == KEYDOWN:
                if Event.key == K_UP:rotate = True
                if Event.key == K_LEFT:dx = -1
                if Event.key == K_RIGHT:dx = 1
                if Event.key == K_ESCAPE: 
                    paused = not paused
                    if (not paused):
                        mixer.music.play()
                if Event.key == K_DOWN:
                    accelarating = True
                    VerticalTicks = time.get_ticks()
                if Event.key == K_RETURN or Event.key ==  K_SPACE:
                    if gameOver:
                        # clear everything
                        for x in range(W):
                                for y in range(H):
                                    area[(x,y)] = False
                        with open(path.join(fileFolder,datafile),"wb") as file:
                            dump(highscore,file)
                        gameOver = False
                        
            if Event.type == KEYUP:
                if Event.key == K_DOWN:
                    accelarating = False

        if accelarating:
            verticalDelay /= 7.5
        keys = key.get_pressed()
        if keys[K_RIGHT]:
            if time.get_ticks() > HorizontalTicks:
                HorizontalTicks = time.get_ticks() + horizontalDelay
                dx = 1
        if keys[K_LEFT]:
            if time.get_ticks() > HorizontalTicks:
                HorizontalTicks = time.get_ticks() + horizontalDelay
                dx = -1

        # calculate shapes
        if not shapeAppeared and not gameOver:
            # calculate new shapes if next shape is not calculated
            if not nextshapeindex:
                shape = newshape(randint(1,7))
            else:
                shape = newshape(nextshapeindex)
            if spaceToSpawn(shape["points"]):
                shapeAppeared = True
            else:
                gameOver = True
            # calculate next shape
            nextshapeindex = randint(1,7)
            nextshape = nextshapes[nextshapeindex]
        
        # screen draw
        screen.blit(bgImage,(0,0))

        # draw score/high-score/lines
        drawText(screen,(415,120),textColor,gameFont,20,f'{lines}',align="center")  # lines
        drawText(screen,(415,220),textColor,gameFont,20,f'{highscore}',align="center")  # hight score
        drawText(screen,(415,295),textColor,gameFont,20,f'{score}',align="center")  # score
        drawText(screen,(415,500),textColor,gameFont,20,f'{Level}',align="center") # level
        # update gameplay
        if not paused and not gameOver:
            # move <-->
            if not collide(shape['points'],deltax = dx):
                for point in shape['points']:
                    point.x += dx

            # move down and row detection
            if time.get_ticks() > VerticalTicks:
                VerticalTicks = time.get_ticks() + verticalDelay
                if collide(shape['points'],deltay = 1):
                    tetromino_placed.play()
                    registerStaticShape(shape['points'])
                    shapeAppeared = False
                    checkrow(shape['points'])
                    if accelarating:
                        score += 100
                    else:
                        score += 50
                    
                if not collide(shape['points'],deltay = 1):
                    for point in shape['points']:
                        point.y += 1

            # rotation
            if rotate:
                if not spaceToRotate(shape["points"]):
                    center = shape['points'][1]
                    for point in shape['points']:
                        x1 = int(center.x - point.x)
                        y1 = int(center.y - point.y)
                        x2 = center.x + y1
                        y2 = center.y - x1
                        point.x,point.y = x2,y2

        # shapes draw
        for point in shape['points']:
            x = point.x * Tile + border
            y = point.y * Tile + border
            screen.blit(shape['tile'],(x,y))

        # static shape draw
        for point in area:
            x = point[0]
            y = point[1]
            if (area[(int(x),int(y))]):
                screen.blit(StaticTileImage,(x*Tile + border,y*Tile + border))
        # nextshape draw
        screen.blit(nextshape,(screen_width-100,screen_height/2+10))
        # game over
        if gameOver:
            # unload current music
            mixer.music.unload()
            # do game over animation
            game_over_animation()
            # clear area
            for point in area:
                area[point] = False

            # reset the Acelaration
            accelarating = False
            if score > highscore:
                highscore_beaten = True
            gameOver = False
            scene = Scene.EndGame
            current_music = None
            return
        # level up
        if lines >= previouslines + LineCheckConstant:
            previouslines = lines

            mixer.music.unload()
            level_up_animation()

            # load music back
            if current_music != "None":
                mixer.music.load(current_music)
                mixer.music.play(-1)

            # reset the Acelaration
            accelarating = False
            if Level <= 15:
                Level+=1
            StaticTileindex += 1
            StaticTileImage = StaticTileColors[StaticTileindex%len(StaticTileColors)]
            
        if paused:
            mixer.music.stop()
            displaymessage("Paused")
        # update display
        display.update()

def AudioSelect():
    global screen,scene,button,current_music
    
    sielenceButton = button(screen_width/2,200,"sielence",35,gameFont,textColor)
    troikaButton = button(screen_width/2,250,"torika",35,gameFont,textColor)
    karnikaButton = button(screen_width/2,300,"karinka",35,gameFont,textColor)
    loginskaButton = button(screen_width/2,350,"loginska",35,gameFont,textColor)
    brandinskyButton = button(screen_width/2,400,"brandinsky",35,gameFont,textColor)
    backButton = button(80,50,"<",40,gameFont,textColor, textalign="topright")
    music_buttons = [
        sielenceButton,
        troikaButton,
        karnikaButton,
        loginskaButton,
        brandinskyButton,
        backButton
    ]
    while True:
        click = False
        for Event in event.get():
            if Event.type == QUIT:
                # close high score before quiting
                with open(path.join(fileFolder,datafile),"wb") as file:
                    dump(max(score,highscore),file)
                quit()
                exit()
            if Event.type == MOUSEBUTTONDOWN:
                click = True
        if sielenceButton.isCMousePointerCollide() and click:current_music = "None"
        if troikaButton.isCMousePointerCollide() and click:current_music = troika
        if karnikaButton.isCMousePointerCollide() and click:current_music = karinka
        if loginskaButton.isCMousePointerCollide() and click:current_music = loginska
        if brandinskyButton.isCMousePointerCollide() and click:current_music = brandinsky
        if backButton.isCMousePointerCollide() and click:
            scene = Scene.MainMenu
            break
        if current_music:
            scene = Scene.RunGame
            break
        screen.blit(EmptyBackground,(0,0))
        drawText(screen, (screen_width/2,120), textColor, gameFont, 40, "select audio", align = "center")
        for _button in music_buttons:
            _button.render()
        display.update()

def MainMenu():
    global screen,scene,button
    playbutton = button(screen_width/2,300,"play",40,gameFont,textColor)
    quitbutton = button(screen_width/2,370,"quit",40,gameFont,textColor)
    mixer.music.load(title)
    mixer.music.play(-1)
    while 1:
        click = 0
        screen.blit(MainMenuImage,(0,0))
        for _event in event.get():
            if _event.type == QUIT:
                # close high score before quiting
                with open(path.join(fileFolder,datafile),"wb") as file:
                    dump(max(score,highscore),file)
                quit()
                exit()
            if _event.type == MOUSEBUTTONDOWN:
                click = 1
        playbutton.render()
        quitbutton.render()
        if playbutton.isCMousePointerCollide() and click:
            scene = Scene.AudioSelect
            break
        if quitbutton.isCMousePointerCollide() and click:
            quit()
            exit()
        display.flip()

if __name__ == "__main__":
    while 1:
        if scene == Scene.MainMenu:
            MainMenu()
            mixer.music.unload()
        elif scene == Scene.EndGame:EndGame()
        elif scene == Scene.RunGame:RunGame()
        else:AudioSelect()
