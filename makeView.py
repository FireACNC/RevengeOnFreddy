from classLogic import *

def makeView(app,screen):
    if app.mode != 'Normal':
        drawTutorial(app,screen)
        return
    drawBg(app,screen)
    drawRoad(app,screen)
    drawScore(app,screen)
    drawHealth(app,screen)
    for object in app.objects: object.draw(screen,app)
    drawGameOver(app,screen)

def drawTutorial(app,screen):
    screen.blit(app.images[app.mode].convert(),(0,0))
    if app.mode == 'tut2':
        screen.blit(app.images['tut2Cover'].convert(),app.coverPos)
    pass

def drawBg(app,screen):
    screen.fill((189, 235, 252))
    bg = app.images['bg']
    screen.blit(bg.convert(),(0,0))

def drawRoad(app,screen):
    color = (255,255,255)
    pygame.draw.polygon(screen,color,[
        (app.roadTopDiff,0),(app.width - app.roadTopDiff,0),
        (app.width-app.roadBotDiff,app.exHeight),(app.roadBotDiff,app.exHeight)
    ])

    numOfPattern = 400
    nextHeight = 5
    nextX,nextY = 0,app.exHeight
    if app.distance%40 < 20: color =(200,200,200)
    for i in range(numOfPattern):
        if (i+app.distance) %40 == 0:
            color = (200,200,200)
        elif (i+app.distance) %20 == 0:
            color = (255,255,255)
        xPos = (app.exHeight-nextY+nextHeight)/app.exHeight*app.roadTopDiff
        pygame.draw.polygon(screen,color,[
            (nextX,nextY),(app.width/2,nextY-nextHeight*34.72741),(app.width-nextX,nextY),
            (app.width-xPos,nextY-nextHeight),(app.width/2,nextY-nextHeight*60.51841),(xPos,nextY-nextHeight)
        ])
        nextY -= nextHeight
        nextHeight *= 0.99442
        nextX = xPos
    pass

def drawScore(app,screen):
    score = app.font.render(f'Score:{app.score}',False,(0,0,0))
    scoreRect = score.get_rect()
    scoreRect.topleft = (20,20)
    screen.blit(score,scoreRect)

def drawHealth(app,screen):
    pygame.draw.rect(screen,(255,255,255),(25,85,300,30),border_radius = 25)
    pygame.draw.rect(screen,(0,255,0),(25,85,app.health,30),border_radius = 25)
    pygame.draw.rect(screen,(7,104,36),(20,80,310,40),width = 5,border_radius = 25)

def drawGameOver(app,screen):
    if app.gameOver:
        pygame.draw.rect(screen,(122,224,134),(0,app.height/2-80,app.width,160))
        word = 'Game over!'
        if app.score < 1000:
            word = 'Well, still not a winner.'
        elif app.score < 10000:
            word = 'Nice try! You can do it!'
        elif app.score < 15000:
            word = 'You beat up Freddy!'
        else:
            word = 'Wait...You must have cheated!'
        score = app.font.render(word,False,(0,0,0))
        scoreRect = score.get_rect()
        scoreRect.center = (app.width/2,app.height/2-5)
        screen.blit(score,scoreRect)
        font2 = pygame.font.Font('TanukiMagic.ttf',20)
        rest = font2.render('Press R to restart.',False,(0,0,0))
        restRect = rest.get_rect()
        restRect.center = (app.width/2,app.height/2+50)
        screen.blit(rest,restRect)