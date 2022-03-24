import pygame as pg
from resources import Button

def pause(paused, screen, window, clock):
    while paused:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    paused = False
                elif event.type == pg.QUIT:
                    pg.quit()
        window.fill("white")
        resume = Button(200, 200, 'Resume', window)
        buttonSprite = pg.sprite.Group()
        buttonSprite.add(resume)
        buttonSprite.draw(window)

        resume.draw_button()
        screen.update()
        clock.Clock().tick(60)     

