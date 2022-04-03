from handTracking import *
from makeView import *
from classLogic import *
from pygame import mixer
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = '640,0'

class App(object):
    pass

pygame.init()
mixer.init()
mixer.music.load('EpicBGM.mp3')

app = App()
makeModel(app)
app.mode = 'tut1'
screen = pygame.display.set_mode((app.width,app.height))
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if app.mode == 'Normal':
                if event.key == pygame.K_r:
                    makeModel(app)
                    mixer.music.stop()
                elif event.key == pygame.K_e:
                    mixer.music.play(loops = -1)
            elif app.mode == 'tut1':
                app.mode = 'tut2'
            elif app.mode == 'tut2':
                app.mode = 'tut3'
            elif app.mode == 'tut3':
                app.mode = 'Normal'
        elif app.mode == 'tut2':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (0< event.pos[0]-app.coverPos[0] < 400) and (
                    0<event.pos[1]-app.coverPos[1] < 280):
                    app.dragPic = True
            elif event.type == pygame.MOUSEMOTION and app.dragPic:
                app.coverPos = (app.coverPos[0] + event.rel[0],
                app.coverPos[1] + event.rel[1])
            elif event.type == pygame.MOUSEBUTTONUP:
                app.dragPic = False
    handMove(app)
    onstep(app)

    makeView(app,screen)
    pygame.display.flip()

    clock.tick(app.FPS)

pygame.quit()
os._exit(0)