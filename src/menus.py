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
    creditos = Button(800, 350, 'Creditos', screen, 'normal')
    quit = Button(800, 500, '  Quit', screen, 'normal')
    # Set background and title
    bg = pg.image.load(os.path.join(BASE_PATH, 'assets/background/main_menu.png'))
    fontDir = os.path.join(BASE_PATH, 'fonts/manaspc.ttf')
    screen.blit(bg, (0,0))
    titleImg1 = pg.font.Font(fontDir, 70).render('Fultano\'s', True, 'black')
    titleImg2 = pg.font.Font(fontDir, 70).render('Tale', True, 'black')
    screen.blit(titleImg1, (50, 50))
    screen.blit(titleImg2, (50, 150))
    # Draw buttons
    quit.drawButton()
    creditos.drawButton()
    # Main menu loop
    while not start:
        # If play button is clicked
        if play.drawButton():
            start = True
            credited = False
        # If credits button is clicked
        if creditos.drawButton():
            credited = True
            start = True
        # Event handler
        for event in pg.event.get():
            # If quit button is clicked
            if event.type == pg.QUIT or quit.drawButton():
                pg.quit()
            # If credits button is clicked
            if creditos.drawButton():
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
    fontDir = 'fonts/manaspc.ttf'
    # Pause menu loop
    while paused:  
        # Set background and text      
        screen.fill((36, 37, 77))
        textImg = pg.font.Font(fontDir, 70).render('Game Paused', True, 'black')
        screen.blit(textImg, (250, 100))
        # Draw the buttons
        quit.drawButton()
        # If resume button is clicked
        if resume.drawButton():
            paused = False
            pg.mixer.music.unpause()
        # Event handler
        for event in pg.event.get():
            # If quit button is clicked
            if event.type == pg.QUIT or quit.drawButton():
                pg.quit()
            # If resume button is clicked or Esc is pressed
            if (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) or resume.drawButton():    
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
    fontDir = 'fonts/manaspc.ttf'
    # Death menu loop
    while start and not restart:
        # Set background and text
        screen.fill((36, 37, 77))
        textImg = pg.font.Font(fontDir, 70).render('Game Over', True, 'black')
        screen.blit(textImg, (300, 100))
        # Draw buttons
        quit.drawButton()
        # If restart button is clicked
        if reset.drawButton():
            restart = True
            dead = False
        # If main menu button is clicked
        if main.drawButton():
            start = False
            dead = False
            pg.mixer.music.unpause()
        # Event handler
        for event in pg.event.get():
            # If quit button is clicked
            if event.type == pg.QUIT or quit.drawButton():
                pg.quit()
            # If main menu button is clicked
            if main.drawButton():    
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
    fontDir = os.path.join(BASE_PATH, 'fonts/manaspc.ttf')
    textCol = pg.Color('black')
    # Credits menu loop
    while(True):   
        # Draw the text
        screen.fill((36, 37, 77))     
        font = pg.font.Font(fontDir, 40)        
        textImg = font.render("Credits", True, textCol)
        textLen = textImg.get_width()
        screen.blit(textImg, (500 - textLen/2, 100))
        font = pg.font.Font(fontDir, 20)
        textImg = font.render("Made by", True, textCol)
        textLen = textImg.get_width()
        screen.blit(textImg, (500 - textLen/2, 200))
        textImg = font.render("Arthur Stevenson", True, textCol)
        textLen = textImg.get_width()
        screen.blit(textImg, (500 - textLen/2, 250))
        textImg = font.render("Eduardo Simplicio", True, textCol)
        textLen = textImg.get_width()
        screen.blit(textImg, (500 - textLen/2, 300))
        textImg = font.render("Matheus Ramos", True, textCol)
        textLen = textImg.get_width()
        screen.blit(textImg, (500 - textLen/2, 350))
        font = pg.font.Font(fontDir, 30)        
        textImg = font.render("Thanks for playing!", True, textCol)
        textLen = textImg.get_width()
        screen.blit(textImg, (500 - textLen/2, 425))
        font = pg.font.Font(fontDir, 15)
        textImg = font.render("Press ESC to get back to main menu", True, textCol)
        textLen = textImg.get_width()
        screen.blit(textImg, (500 - textLen/2, 465))
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
    fontDir = 'fonts/manaspc.ttf'
    # Win menu loop
    while start:
        # Set background and text
        screen.fill((36, 37, 77))
        textImg = pg.font.Font(fontDir, 70).render(' You Won!', True, 'black')
        screen.blit(textImg, (300, 100))
        # Draw buttons
        quit.drawButton()
        # If main menu button is clicked
        if main.drawButton():
            start = False
            pg.mixer.music.unpause()
        # Event handler
        for event in pg.event.get():
            if event.type == pg.QUIT or quit.drawButton():
                pg.quit()
            # If main menu button is clicked
            if main.drawButton():    
                start = False
        # Update screen and time
        pg.display.update()
        clock.Clock().tick(60)
    return start