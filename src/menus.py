import pygame as pg
import os
from resources import Button
from utils import BASE_PATH


def main(start, screen, clock, credited):
    play = Button(800, 200, '   Play', screen, 'large')
    creditos = Button(800, 350, 'Creditos', screen, 'normal')
    quit = Button(800, 500, '  Quit', screen, 'normal')
    bg = pg.image.load(os.path.join(BASE_PATH, 'assets/background/main_menu.png'))
    fontDir = os.path.join(BASE_PATH, 'fonts/manaspc.ttf')
    screen.blit(bg, (0,0))
    title_img1 = pg.font.Font(fontDir, 70).render('Fultano\'s', True, 'black')
    title_img2 = pg.font.Font(fontDir, 70).render('Tale', True, 'black')
    screen.blit(title_img1, (50, 50))
    screen.blit(title_img2, (50, 150))
    quit.draw_button()
    creditos.draw_button()
    while not start:
        if play.draw_button():
            start = True
            credited = False
        if creditos.draw_button():
            credited = True
            start = True
        for event in pg.event.get():
            if event.type == pg.QUIT or quit.draw_button():
                pg.quit()
            if creditos.draw_button():
                credited = True
                start = True
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                start = True
                credited = False
        pg.display.update()
        clock.Clock().tick(60)
    return start, credited

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

def death(start, screen, clock, restart, dead):
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
            dead = False
        if main.draw_button():
            start = False
            dead = False
            pg.mixer.music.unpause()
        for event in pg.event.get():
            if event.type == pg.QUIT or quit.draw_button():
                pg.quit()
            if main.draw_button():    
                start = False
                dead = False
        pg.display.update()
        clock.Clock().tick(60)
    return start, restart, dead

def authors(window):
    fontDir = os.path.join(BASE_PATH, 'fonts/manaspc.ttf')
    text_col = pg.Color('black')
    while(True):   
        window.fill((36, 37, 77))     
        font = pg.font.Font(fontDir, 40)        
        text_img = font.render("Credits", True, text_col)
        text_len = text_img.get_width()
        window.blit(text_img, (500 - text_len/2, 100))
        font = pg.font.Font(fontDir, 20)
        text_img = font.render("Made by", True, text_col)
        text_len = text_img.get_width()
        window.blit(text_img, (500 - text_len/2, 200))
        text_img = font.render("Arthur Stevenson", True, text_col)
        text_len = text_img.get_width()
        window.blit(text_img, (500 - text_len/2, 250))
        text_img = font.render("Eduardo Simplicio", True, text_col)
        text_len = text_img.get_width()
        window.blit(text_img, (500 - text_len/2, 300))
        text_img = font.render("Matheus Ramos", True, text_col)
        text_len = text_img.get_width()
        window.blit(text_img, (500 - text_len/2, 350))
        font = pg.font.Font(fontDir, 30)        
        text_img = font.render("Thanks for playing!", True, text_col)
        text_len = text_img.get_width()
        window.blit(text_img, (500 - text_len/2, 425))
        font = pg.font.Font(fontDir, 15)
        text_img = font.render("Press ESC to get back to main menu", True, text_col)
        text_len = text_img.get_width()
        window.blit(text_img, (500 - text_len/2, 465))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                print("quit")
                pg.quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                print("esc")
                return False, False
        pg.display.update()