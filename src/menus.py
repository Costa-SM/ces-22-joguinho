import pygame as pg
from sympy import im
import os
from resources import Button
from utils import FONTS_DIR

fontDir = os.path.join(FONTS_DIR, 'manaspc.ttf')

def main(start, screen, window, clock):
    play = Button(500, 400, ' Play', window)
    window.fill((28, 48, 111))
    text_img = pg.font.Font(fontDir, 50).render('Fultano\'s Tale', True, 'black')
    window.blit(text_img, (275, 100))
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
        text_img = pg.font.Font(fontDir, 40).render('Game Paused', True, 'black')
        window.blit(text_img, (350, 200))
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

