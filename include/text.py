import pygame as pg

class Text:
    """Per facilitare il renderizzamento del testo a schermo"""
    def __init__(self, text, size=20, color=(255,255,255)):
        font = pg.font.SysFont("Times new roman", size, bold = True)
        self.text = font.render(text, True, color)
        self.string = text
        self.rect = self.text.get_rect()
        self.size = font.size(text)

    def render(self, screen, color, *position):
        """Si ha la possibilità di specificare il centro del testo,
        mettendo come ultimo parametro qualsiasi cosa, tipicamente un 'center'
        """
        if position:
            if len(position) > 2:
                self.rect.center = position[:2]
            else:
                self.rect.x, self.rect.y = position
        else:
            self.rect.center = (screen.get_width()/2, screen.get_height()/2)
            
        if color:
            s = pg.Surface(screen.get_size(),pg.SRCALPHA)
            pg.draw.rect(s, color, s.get_rect())
            screen.blit(s, (0,0))

        screen.blit(self.text, self.rect)
