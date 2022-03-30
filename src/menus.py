from pdb import Restart
import pygame as pg
import os
from resources import Button

def main(start, screen, clock):
    play = Button(400, 400, ' Play', screen)
    quit = Button(600, 400, ' Quit', screen)
    fontDir = 'fonts/manaspc.ttf'
    screen.fill((36, 37, 77))
    text_img = pg.font.Font(fontDir, 50).render('Fultano\'s Tale', True, 'black')
    screen.blit(text_img, (275, 100))
    quit.draw_button()
    while not start:
        if play.draw_button():
            start = True
        for event in pg.event.get():
            if event.type == pg.QUIT or quit.draw_button():
                pg.quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                start = True
        pg.display.update()
        clock.Clock().tick(60)
    
    return start 

def pause(paused, screen, clock):
    resume = Button(400, 400, 'Resume', screen)
    quit = Button(600, 400, ' Quit', screen)
    fontDir = 'fonts/manaspc.ttf'
    while paused:        
        screen.fill((36, 37, 77))
        text_img = pg.font.Font(fontDir, 40).render('Game Paused', True, 'black')
        screen.blit(text_img, (350, 200))
        quit.draw_button()
        if resume.draw_button():
            paused = False
            pg.mixer.music.unpause()
        for event in pg.event.get():
            if event.type == pg.QUIT or quit.draw_button():
                pg.quit()
            if (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) or resume.draw_button():    
                paused = False
                pg.mixer.music.unpause()
        pg.display.update()
        clock.Clock().tick(60)
    return paused

def death(start, screen, clock):
    restart = Button(400, 400, 'Main Menu', screen)
    quit = Button(600, 400, ' Quit', screen)
    fontDir = 'fonts/manaspc.ttf'
    while start:
        screen.fill((36, 37, 77))
        text_img = pg.font.Font(fontDir, 40).render('Game Over', True, 'black')
        screen.blit(text_img, (350, 200))
        quit.draw_button()
        if restart.draw_button():
            start = False
            pg.mixer.music.unpause()
        for event in pg.event.get():
            if event.type == pg.QUIT or quit.draw_button():
                pg.quit()
            if (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) or restart.draw_button():    
                start = False
                pg.mixer.music.unpause()
        pg.display.update()
        clock.Clock().tick(60)
    return start