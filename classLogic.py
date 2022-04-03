import pygame, random

class Player(pygame.sprite.Sprite):
    def __init__(self,app):
        self.cy = app.handY
        self.cx = app.handX
        self.r = 80
    
    def update(self,app):
        self.cx = app.handX
        self.cx = max(self.cx,60)
        self.cx = min(self.cx,980)

    def draw(self,screen,app):
        imgSuf = app.currImg.convert_alpha()
        imgRect = imgSuf.get_rect()
        imgRect.center = (self.cx,self.cy)
        screen.blit(imgSuf,imgRect)

class Mob(pygame.sprite.Sprite):
    def __init__(self,app):
        self.distance = 0
        self.moveTimes = 100
        topLength = app.width-2*app.roadTopDiff
        #How much the spawned mob is deviated from the left top corner
        self.xDiv = random.randint(0,topLength)
        self.initX = app.roadTopDiff+self.xDiv
        self.cx,self.cy = self.initX,0
        self.r = 5
        endX = self.xDiv /  topLength * app.exWidth - (app.exWidth-app.width)
        self.dx = (endX - self.cx)/app.exHeight
        self.dy = 2.711
        self.dr = 0.3

        self.scale = 1.0234

    def update(self,app):
        self.distance += 1
        if self.distance > self.moveTimes or self.cy < 0: 
            app.objects.remove(self)
            return
        #Find the distance moved each time
        self.cx += self.dx*self.dy
        self.cy += self.dy
        self.r += self.dr
        self.dy *= self.scale
        self.dr *= self.scale

        if 0 <= (app.handY - self.cy) <= 20 and abs(self.cx - app.handX) <= 60:
            app.gameOver = True
            return
        if self.cy > app.handY and app.objects.index(self) < app.objects.index(app.player):
            app.objects.remove(self)
            app.objects.insert(app.objects.index(app.player)+1,self)
        pass

    def draw(self,screen,app):
        #I am not using any recursion!!! Just HARDCODE one freddy!!!!!
        pygame.draw.circle(screen,(0,0,0),(self.cx,self.cy),self.r*1.05)
        pygame.draw.circle(screen,(0,0,0),(self.cx-self.r/3,self.cy+self.r*0.25),self.r*0.85)
        pygame.draw.circle(screen,(0,0,0),(self.cx+self.r/3,self.cy+self.r*0.25),self.r*0.85)
        pygame.draw.circle(screen,(0,0,0),(self.cx-self.r*0.8,self.cy-self.r*0.9),self.r*0.45)
        pygame.draw.circle(screen,(0,0,0),(self.cx+self.r*0.8,self.cy-self.r*0.9),self.r*0.45)
        pygame.draw.circle(screen,(188,125,110),(self.cx,self.cy),self.r)
        pygame.draw.circle(screen,(188,125,110),(self.cx-self.r/3,self.cy+self.r*0.25),self.r*0.8)
        pygame.draw.circle(screen,(188,125,110),(self.cx+self.r/3,self.cy+self.r*0.25),self.r*0.8)
        pygame.draw.circle(screen,(188,125,110),(self.cx-self.r*0.8,self.cy-self.r*0.9),self.r*0.4)
        pygame.draw.circle(screen,(188,125,110),(self.cx+self.r*0.8,self.cy-self.r*0.9),self.r*0.4)
        pygame.draw.circle(screen,(0,0,0),(self.cx-self.r/2,self.cy-self.r/3),self.r/5)
        pygame.draw.circle(screen,(0,0,0),(self.cx+self.r/2,self.cy-self.r/3),self.r/5)
        pygame.draw.circle(screen,(231,206,204),(self.cx,self.cy+self.r/3),self.r*0.7)
        nozeRadius = self.r/5
        pygame.draw.polygon(screen,(188,125,110),[
            (self.cx-nozeRadius,self.cy),(self.cx+nozeRadius,self.cy),(self.cx,self.cy+nozeRadius*1.6)])

        pass

################################################################################

def makeModel(app):
    app.exWidth, app.exHeight = 1040,800
    app.width, app.height = 1040,620
    app.FPS = 60
    app.handChoice = 'Right' 
    app.handEventSet = set()
    app.roadTopDiff = 450
    app.roadBotDiff = 0
    app.score = 0
    app.font = pygame.font.Font('TanukiMagic.ttf',50)
    app.mode = 'Normal'
    #Walk is for which foot is moves, while walking track the remaining power of walking
    #Walking per move is how much power will one move of finger provide
    app.walk = None
    app.walking = 0
    app.walkingPerMove = 10
    app.attack = False
    app.hi = False
    app.objects = []
    app.handX = app.width/2
    app.handY = app.exHeight*0.6
    for i in range(random.randint(4,6)):
        mob = Mob(app)
        for j in range(random.randint(i*10,(i+1)*10)):
            mob.update(app)
        app.objects.append(mob)
    app.player = Player(app)
    app.objects.append(app.player)
    app.distance = 0

    app.gameOver = False
    app.images = {}
    for imageName in ['bg','hi','ready','attack',
        'walk1','walk2','walk3','walk4',
        'tut1','tut2','tut2Cover','tut3']:
        app.images[imageName] = pygame.image.load(f'pics/{imageName}.png')
    app.currImg = app.images['hi']
    app.coverPos = (570,25)
    app.dragPic = False
    app.tick = 0
    app.mode = 'Normal'
    app.health = 300

def onstep(app):
    if app.gameOver:
        pass
    elif app.mode in ['tut1','tut2','tut3']:
        app.handEventSet = set()
    else:
        eventHandler(app)
        if app.walking > 0:
            app.walking -= 1
            app.score += 5
            app.distance += 5
            #Control the amount of mob created
            if random.randint(1,25) == 25 and len(app.objects)<12:
                app.objects.insert(0,Mob(app))
            elif len(app.objects) < 5:
                app.objects.insert(0,Mob(app))
            for object in app.objects[::-1]: object.update(app)
        if app.tick%5 == 0:
            if app.walking: app.health -= 1
            imgUpdate(app)
            if app.health <= 0: app.gameOver = True
        app.FPS = 60 + app.score//1000

def attack(app):
    for object in app.objects[::-1]:
        if type(object) == Mob:
            if (app.handY-object.cy) < 100 and abs(object.cx - app.handX) < 100:
                object.dy *= -5
                object.dx *= -5
                app.score += 200
                app.health = min(300,app.health + 10)

    pass

def eventHandler(app):
    if 'Attack' in app.handEventSet:
        if not app.attack: 
            attack(app)
        app.attack = True
    elif 'Hi' in app.handEventSet:
        app.hi = True
    else:
        app.attack = app.hi = False
    if 'Left' in app.handEventSet:
        if app.walk != 'Left':
            app.walking = max(app.walking,app.walkingPerMove)
        app.walk = 'Left'
    elif 'Right' in app.handEventSet:
        if app.walk != 'Right':
            app.walking = max(app.walking,app.walkingPerMove)
        app.walk = 'Right'
    app.handEventSet = set()

#some animation part
def imgUpdate(app):
    if app.attack:
        app.currImg = app.images['attack']
    elif app.hi:
        app.currImg = app.images['hi']
    elif app.walking > 0:
        if app.walk == 'Left':
            if app.currImg == app.images['walk1']:
                app.currImg = app.images['walk2']
            elif app.currImg == app.images['walk3'] or app.currImg == app.images['walk4']:
                app.currImg = app.images['walk4']
            else:
                app.currImg = app.images['walk3']
        elif app.walk == 'Right':
            if app.currImg == app.images['walk4']:
                app.currImg = app.images['walk3']
            elif app.currImg == app.images['walk2'] or app.currImg == app.images['walk1']:
                app.currImg = app.images['walk1']
            else:
                app.currImg = app.images['walk2']
    else:
        if app.currImg == app.images['walk1']:
                app.currImg = app.images['walk2']
        elif app.currImg == app.images['walk4']:
                app.currImg = app.images['walk3']
        else: app.currImg = app.images['ready']
