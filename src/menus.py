import pygame as pg
import os
from resources import Button
from utils import BASE_PATH

def main(start, screen, clock):
    play = Button(800, 200, '   Play', screen, 'large')
    settings = Button(800, 350, 'Settings', screen, 'normal')
    quit = Button(800, 500, '  Quit', screen, 'normal')
    bg = pg.image.load(os.path.join(BASE_PATH, 'assets/background/main_menu.png'))
    fontDir = os.path.join(BASE_PATH, 'fonts/manaspc.ttf')
    screen.blit(bg, (0,0))
    title_img1 = pg.font.Font(fontDir, 70).render('Fultano\'s', True, 'black')
    title_img2 = pg.font.Font(fontDir, 70).render('Tale', True, 'black')
    screen.blit(title_img1, (50, 50))
    screen.blit(title_img2, (50, 150))
    quit.draw_button()
    settings.draw_button()
    while not start:
        if play.draw_button():
            start = True
        for event in pg.event.get():
            if event.type == pg.QUIT or quit.draw_button():
                pg.quit()
            if settings.draw_button():
                pass #TODO
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                start = True
        pg.display.update()
        clock.Clock().tick(60)
    
    return start 

def pause(paused, screen, clock):
    resume = Button(500, 300, ' Resume', screen, 'normal')
    quit = Button(500, 450, '  Quit', screen, 'normal')
    fontDir = 'fonts/manaspc.ttf'
    while paused:        
        screen.fill((36, 37, 77))
        text_img = pg.font.Font(fontDir, 70).render('Game Paused', True, 'black')
        screen.blit(text_img, (250, 100))
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

def death(start, screen, clock, restart):
    main = Button(500, 300, '  Menu', screen, 'normal')
    reset = Button(500, 400, ' Restart', screen, 'normal')
    quit = Button(500, 500, '  Quit', screen, 'normal')
    fontDir = 'fonts/manaspc.ttf'
    while start and not restart:
        screen.fill((36, 37, 77))
        text_img = pg.font.Font(fontDir, 70).render('Game Over', True, 'black')
        screen.blit(text_img, (300, 100))
        quit.draw_button()
        if reset.draw_button():
            restart = True
        if main.draw_button():
            start = False
            pg.mixer.music.unpause()
        for event in pg.event.get():
            if event.type == pg.QUIT or quit.draw_button():
                pg.quit()
            if (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) or main.draw_button():    
                start = False
                pg.mixer.music.unpause()
        pg.display.update()
        clock.Clock().tick(60)
    return start, restart