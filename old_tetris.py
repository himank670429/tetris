from pygame import *
from random import choice, randint
from os import path,listdir
from pickle import load,dump

# initialize
init()
font.init()
mixer.init()

vec = math.Vector2
shape = 0
TileImage = 0
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
score = 0
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
gameOverDuration = 10000
shapeAppeared = False

score_pop_up_pos = (0,0)
score_pop_up_ticks = 0
score_pop_up_delay = 300
is_score_poping_out = False

# scores
lines = 0
highscore = 0
score = 0

current_music = None

screen = display.set_mode((screen_width, screen_height))

area = {}
for x in range(W):
    for y in range(H):
        area[(x,y)] = False

# folder and file paths
fileFolder = path.dirname(__file__)
AssetsFolder = path.join(fileFolder,"Assets")
spritesFolder = path.join(AssetsFolder,"sprites")
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
messageboxImage = image.load(path.join(GUIfolder,"messagebox.png"))
messageboxImage = transform.scale(messageboxImage,(_W,_H))

# font loading
gameFont = path.join(FontFolder,"gameFont.ttf")

# musics
troika = path.join(soundfolder,"Torika.mp3")
brandinsky = path.join(soundfolder,"Brandinsky.mp3")
loginska = path.join(soundfolder,"Loginska.mp3")
karinka = path.join(soundfolder,"Karinka.mp3")
level_up = path.join(soundfolder,"Level Up.mp3")
level_clear = path.join(soundfolder,"Level clear.mp3")
title = path.join(soundfolder,choice(["title theme 1.mp3", "title theme 2.mp3"]))
game_over = path.join(soundfolder,"Game Over.mp3")

# SFX
tetromino_placed = mixer.Sound(path.join(soundfolder, "tetromino placed.mp3"))
line_cleared = mixer.Sound(path.join(soundfolder, "line clear.mp3"))



TileSprites = {
    "shape01":{"shape":[(0,0),(0,1),(0,2),(0,3)],"tile":redTile},
    "shape02":{"shape":[(0,0),(0,1),(1,0),(1,1)],"tile":blueTile},
    "shape03":{"shape":[(0,0),(0,1),(0,2),(1,1)],"tile":brownTile},
    "shape04":{"shape":[(1,0),(1,1),(0,1),(0,2)],"tile":cyanTile},
    "shape05":{"shape":[(0,0),(0,1),(0,2),(1,2)],"tile":pinkTile},
    "shape06":{"shape":[(0,0),(0,1),(1,1),(1,2)],"tile":greenTile},
    "shape07":{"shape":[(1,0),(1,1),(1,2),(0,2)],"tile":orangeTile}
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

def newshape(index):
    global TileImage
    shape = []
    sprite = choice([s for s in TileSprites])
    tileshape = TileSprites[sprite]["shape"]
    TileImage = TileSprites[sprite]["tile"]
    offset = randint(4,5)
    for point in tileshape:
        x = point[0]+offset
        y = point[1]
        shape.append(vec(x,y))
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
    global lines
    y = max([point.y for point in shape])
    for dy in range(4):
        _y = y - dy
        if _y < 0:
            return
        while isRowAppear(_y):
            deleteRow(_y)
            line_cleared.play()
            updatestaticshape(_y)
            lines += 1

def deleteRow(y):
    for x in range(W):
        area[(x,y)] = False

def isRowAppear(y):
    for x in range(W):
        if not area[(x,y)]:
            return False
    return True

def spaceToRotate(shape_):
    center = shape_[1]
    for point in shape:
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
        # screen.blit(bgImage,(0,0))
        # drawText(screen,(415,120),textColor,gameFont,20,f'{lines}',align="center")  # lines
        # drawText(screen,(415,220),textColor,gameFont,20,f'{highscore}',align="center")  # high score
        # drawText(screen,(415,295),textColor,gameFont,20,f'{score}',align="center")  # score
        display.update()
        for Event in event.get():
            if Event.type == QUIT:
                exit()
            if Event.type == KEYDOWN:
                if Event.key == K_SPACE or Event.key == K_RETURN:
                    mixer.music.unload()
                    return
        now = time.get_ticks()

def level_up_animation():
    global level_up_animation_tick,accelarating
    start = time.get_ticks()
    now = time.get_ticks()
    mixer.music.load(level_up)
    mixer.music.play()
    while (now-start < level_up_message_tick):
        screen.blit(bgImage,(0,0))
        drawText(screen,(415,120),textColor,gameFont,20,f'{lines}',align="center")  # lines
        drawText(screen,(415,220),textColor,gameFont,20,f'{highscore}',align="center")  # high score
        drawText(screen,(415,295),textColor,gameFont,20,f'{score}',align="center")  # score
        displaymessage("level up")
        for Event in event.get():
            if Event.type == QUIT:
                quit()
                exit()
            if Event.type == KEYDOWN:
                return
        display.update()

# loading stuff
with open(path.join(fileFolder,datafile),"rb") as file:
    highscore = load(file)

# scenes
def RunGame():
    global HorizontalTicks,VerticalTicks,shapeAppeared,score,gameOver,paused,shape,accelarating,Level,lines,previouslines,LineCheckConstant,score,highscore,StaticTileImage,StaticTileColors,StaticTileindex,current_music, scene
    if current_music != "None":
        mixer.music.load(current_music)
        mixer.music.play(-1)
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
                    dump(highscore,file)
                exit()
            if Event.type == KEYDOWN:
                if Event.key == K_UP:rotate = True
                if Event.key == K_LEFT:dx = -1
                if Event.key == K_RIGHT:dx = 1
                if Event.key == K_ESCAPE: paused = not paused
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
            index = randint(0,6)
            shape = newshape(index)
            if spaceToSpawn(shape):
                shapeAppeared = True
            else:
                gameOver = True

        
        # screen draw
        screen.blit(bgImage,(0,0))
        
        # draw score/high-score/lines
        drawText(screen,(415,120),textColor,gameFont,20,f'{lines}',align="center")  # lines
        drawText(screen,(415,220),textColor,gameFont,20,f'{highscore}',align="center")  # hight score
        drawText(screen,(415,295),textColor,gameFont,20,f'{score}',align="center")  # score
        # update gameplay
        if not paused and not gameOver:
            # move <-->
            if not collide(shape,deltax = dx):
                for point in shape:
                    point.x += dx

            # move down and row detection
            if time.get_ticks() > VerticalTicks:
                VerticalTicks = time.get_ticks() + verticalDelay
                if collide(shape,deltay = 1):
                    tetromino_placed.play()
                    registerStaticShape(shape)
                    shapeAppeared = False
                    checkrow(shape)
                    score += 50
                    
                if not collide(shape,deltay = 1):
                    for point in shape:
                        point.y += 1

            # rotation
            if rotate:
                if not spaceToRotate(shape):
                    center = shape[1]
                    for point in shape:
                        x1 = int(center.x - point.x)
                        y1 = int(center.y - point.y)
                        x2 = center.x + y1
                        y2 = center.y - x1
                        point.x,point.y = x2,y2

        # shapes draw
        for point in shape:
            x = point.x * Tile + border
            y = point.y * Tile + border
            screen.blit(TileImage,(x,y))

        # static shape draw
        for point in area:
            x = point[0]
            y = point[1]
            if (area[(int(x),int(y))]):
                screen.blit(StaticTileImage,(x*Tile + border,y*Tile + border))
        # game over
        if gameOver:
            # unload current music
            mixer.music.unload()
            # do game over animation
            game_over_animation()
            # clear area
            for point in area:
                area[point] = False
            # load music back
            if current_music != "None":
                mixer.music.load(current_music)
                mixer.music.play(-1)

            # reset the Acelaration
            accelarating = False
            if score > highscore:
                highscore = score
            score = 0
            gameOver = False
            scene = Scene.AudioSelect
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
            break
        display.flip()
        
while 1:
    if scene == Scene.MainMenu:
        MainMenu()
        mixer.music.unload()
    elif scene == Scene.RunGame:RunGame()
    else:AudioSelect()