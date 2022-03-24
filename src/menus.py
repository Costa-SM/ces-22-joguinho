import pygame as pg
from resources import Button


def main(start, screen, window, clock):
    play = Button(500, 400, ' Play', window)
    window.fill((28, 48, 111))
    while not start:
        if play.draw_button():
            start = True
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
        screen.update()
        clock.Clock().tick(60)
    
    return start 



def pause(paused, screen, window, clock):
    resume = Button(500, 400, 'Resume', window)
    while paused:
        window.fill((28, 48, 111))
        if resume.draw_button():
            paused = False  
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) or resume.draw_button():    
                paused = False
        screen.update()
        clock.Clock().tick(60)
    return paused

