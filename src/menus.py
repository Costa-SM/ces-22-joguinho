import pygame as pg
import os
from resources import Button
from utils import BASE_PATH

def main(start, screen, clock, credited):
    '''
    Function that creates the main menu.
    :param start: whether the game started or not
    :type start: bool
    :param screen: game screen
    :type screen: pg.display
    :param clock: game time
    :type clock: pg.Time
    :param credited: whether the credit screen is showing or not
    :type credited: bool
    :rtype: bool, bool

    '''
    # Create each button
    play = Button(800, 200, '   Play', screen, 'large')
    creditos = Button(800, 350, 'Credits', screen, 'normal')
    quit = Button(800, 500, '  Quit', screen, 'normal')
    # Set background and title
    bg = pg.image.load(os.path.join(BASE_PATH, 'assets/background/main_menu.png'))
    font_dir = os.path.join(BASE_PATH, 'fonts/manaspc.ttf')
    screen.blit(bg, (0,0))
    title_img_1 = pg.font.Font(font_dir, 70).render('Fultano\'s', True, 'black')
    title_img_2 = pg.font.Font(font_dir, 70).render('Tale', True, 'black')
    screen.blit(title_img_1, (50, 50))
    screen.blit(title_img_2, (50, 150))
    # Draw buttons
    quit.draw_button()
    creditos.draw_button()
    # Main menu loop
    while not start:
        # If play button is clicked
        if play.draw_button():
            start = True
            credited = False
        # If credits button is clicked
        if creditos.draw_button():
            credited = True
            start = True
        # Event handler
        for event in pg.event.get():
            # If quit button is clicked
            if event.type == pg.QUIT or quit.draw_button():
                pg.quit()
            # If credits button is clicked
            if creditos.draw_button():
                credited = True
                start = True
            # If enter is pressed
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                start = True
                credited = False
        # Update screen and time
        pg.display.update()
        clock.Clock().tick(60)
    return start, credited

def pause(paused, screen, clock):
    '''
    Function that creates the pause menu.
    :param paused: whether the game has been paused or not
    :type paused: bool
    :param screen: game screen
    :type screen: pg.display
    :param clock: game time
    :type clock: pg.Time
    :rtype: bool

    '''
    # Create each button
    resume = Button(500, 300, ' Resume', screen, 'normal')
    quit = Button(500, 450, '  Quit', screen, 'normal')
    # Set font
    font_dir = 'fonts/manaspc.ttf'
    # Pause menu loop
    while paused:  
        # Set background and text      
        screen.fill((36, 37, 77))
        text_img = pg.font.Font(font_dir, 70).render('Game Paused', True, 'black')
        screen.blit(text_img, (250, 100))
        # Draw the buttons
        quit.draw_button()
        # If resume button is clicked
        if resume.draw_button():
            paused = False
            pg.mixer.music.unpause()
        # Event handler
        for event in pg.event.get():
            # If quit button is clicked
            if event.type == pg.QUIT or quit.draw_button():
                pg.quit()
            # If resume button is clicked or Esc is pressed
            if (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) or resume.draw_button():
                paused = False
                pg.mixer.music.unpause()
        # Update screen and time
        pg.display.update()
        clock.Clock().tick(60)
    return paused

def death(start, screen, clock, restart, dead):
    '''
    Function that creates the death menu.
    :param start: whether the game started or not
    :type start: bool
    :param screen: game screen
    :type screen: pg.display
    :param clock: game time
    :type clock: pg.Time
    :param restart: whether the game restarted or not
    :type restart: bool
    :param dead: whether the player is dead or not
    :type dead: bool
    :rtype: bool, bool, bool

    '''
    # Create the buttons
    main = Button(500, 300, '  Menu', screen, 'normal')
    reset = Button(500, 400, ' Restart', screen, 'normal')
    quit = Button(500, 500, '  Quit', screen, 'normal')
    # Set font
    font_dir = 'fonts/manaspc.ttf'
    # Death menu loop
    while start and not restart:
        # Set background and text
        screen.fill((36, 37, 77))
        text_img = pg.font.Font(font_dir, 70).render('Game Over', True, 'black')
        screen.blit(text_img, (300, 100))
        # Draw buttons
        quit.draw_button()
        # If restart button is clicked
        if reset.draw_button():
            restart = True
            dead = False
        # If main menu button is clicked
        if main.draw_button():
            start = False
            dead = False
            pg.mixer.music.unpause()
        # Event handler
        for event in pg.event.get():
            # If quit button is clicked
            if event.type == pg.QUIT or quit.draw_button():
                pg.quit()
            # If main menu button is clicked
            if main.draw_button():
                start = False
                dead = False
        # Update display and time
        pg.display.update()
        clock.Clock().tick(60)
    return start, restart, dead

def authors(screen):
    '''
    Function that creates credits menu
    :param screen: game screen
    :type screen: pg.display
    :rtype: bool, bool

    '''
    # Set font
    font_dir = os.path.join(BASE_PATH, 'fonts/manaspc.ttf')
    text_col = pg.Color('black')
    # Credits menu loop
    while(True):
        # Draw the text
        screen.fill((36, 37, 77))
        font = pg.font.Font(font_dir, 40)
        text_img = font.render("Credits", True, text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (500 - text_len/2, 100))
        font = pg.font.Font(font_dir, 20)
        text_img = font.render("Made by", True, text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (500 - text_len/2, 200))
        text_img = font.render("Arthur Stevenson", True, text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (500 - text_len/2, 250))
        text_img = font.render("Eduardo Simplicio", True, text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (500 - text_len/2, 300))
        text_img = font.render("Matheus Ramos", True, text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (500 - text_len/2, 350))
        font = pg.font.Font(font_dir, 30)        
        text_img = font.render("Thanks for playing!", True, text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (500 - text_len/2, 425))
        font = pg.font.Font(font_dir, 15)
        text_img = font.render("Press ESC to get back to main menu", True, text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (500 - text_len/2, 465))
        # Event handler
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return False, False
        # Update screen
        pg.display.update()

def win(start, screen, clock):
    '''
    Function that creates the win menu.
    :param start: whether the game has started not
    :type start: bool
    :param screen: game screen
    :type screen: pg.display
    :param clock: game time
    :type clock: pg.Time
    :rtype: bool

    '''
    # Create the buttons
    main = Button(500, 300, '  Menu', screen, 'normal')
    quit = Button(500, 450, '  Quit', screen, 'normal')
    # Set font
    font_dir = 'fonts/manaspc.ttf'
    # Win menu loop
    while start:
        # Set background and text
        screen.fill((36, 37, 77))
        text_img = pg.font.Font(font_dir, 70).render(' You Won!', True, 'black')
        screen.blit(text_img, (300, 100))
        # Draw buttons
        quit.draw_button()
        # If main menu button is clicked
        if main.draw_button():
            start = False
            pg.mixer.music.unpause()
        # Event handler
        for event in pg.event.get():
            if event.type == pg.QUIT or quit.draw_button():
                pg.quit()
            # If main menu button is clicked
            if main.draw_button():    
                start = False
        # Update screen and time
        pg.display.update()
        clock.Clock().tick(60)
    return start