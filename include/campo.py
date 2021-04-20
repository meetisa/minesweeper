import pygame as pg
import spritesheet
from random import choice
from funzione import os_command

class Campo:
    def __init__(self):
        """Classe per il campo"""
        self.surfs = spritesheet.SpriteSheet('src/tiles.jpg').load_strip((0,0,32,32),12)

    def build(self, screen, n_mine):
        """Per costuire il campo di gioco,
        per piazzare le mine e quindi calcolare quale
        numero avrà ogni quadrato
        """
        self.mine = n_mine
        self.columns = range(int(screen.get_width()/32))
        self.raws = range(int(screen.get_height()/32))

        self.done = False
        self.nflags = 0

        # Il campo è costituito da due layer differenti:
        # Quello più sopra sono i quadrati inizilali, tutti uguali, che nasconde il secondo;
        # Quello più sotto è formato da quadrati con numeri, mine oppure sono vuoti.

        self.sopra = [[10 for column in self.columns] for raw in self.raws]

        # All'inizio il secondo layer è vuoto
        self.sotto = [[0 for column in self.columns] for raw in self.raws]

        self.mouse_is_there = [[False for _ in self.columns] for raw in self.raws]


        # Posizione le mine in modo randomico
        for _ in range(n_mine):
            
            # secondo ciclo per evitare di ripetere delle coordinate
            while True:
                r = choice(self.raws)
                c = choice(self.columns)
                if self.sotto[r][c] != 9:
                    self.sotto[r][c] = 9
                    break

        # Calcolo tutti i rect dei quadrati, partendo dall'angolo in alto a sinitra
        x_square = 0
        y_square = 0
        self.rect = []
        for raw in self.raws:
            self.rect.append([])
            for column in self.columns:

                # Analizzo il quadrato:
                if self.sotto[raw][column] == 0:
                    # Uso una funzione della classe che restituisce
                    # i valori o le coordinate di tutti i quadrati adiacenti
                    # al quadrato delle coordinate date
                    mine = sum([1 for square in self.borders(raw,column,'values') if square == 9])
                    
                    self.sotto[raw][column] = mine
                    
                self.rect[-1].append(pg.Rect(x_square, y_square, 32, 32))
                x_square += 32
            x_square = 0
            y_square += 32


    def update(self, event):
        """In questa funzione vengono analizzati tutti
        gli eventi che il giocatore provoca:
        in questo caso bisogna occuparsi solo di quando
        clicca il mouse
        """
        for ir in self.raws:
            for ic in self.columns:
                sopra = self.sopra[ir][ic]
                sotto = self.sotto[ir][ic]
                    
                # Rilevo in quale quadrato è posizionato il cursore
                if self.rect[ir][ic].collidepoint(pg.mouse.get_pos()):

                    self.mouse_is_there[ir][ic] = True

                    # Rivelo se il giocatore ha premuto un tasto del mouse
                    if event.type == pg.MOUSEBUTTONDOWN:

                        # Se si preme il tasto sinistro
                        if event.button == 1 and sopra == 10:
                            if self.scopre(ir,ic):
                                pg.time.delay(1000)
                                self.done = True
                                return 'perdita'

                        # Se si preme il tasto centrale (rotella)
                        if event.button == 2:
                            if 0 < sopra < 9:
                                for ir2, ic2 in self.borders(ir,ic,'indexes'):
                                    if self.sopra[ir2][ic2] != 11:
                                        if self.scopre(ir2,ic2):
                                            pg.time.delay(1000)
                                            self.done = True
                                            return 'perdita'
                                        else:
                                            self.sopra[ir2][ic2] = self.sotto[ir2][ic2]

                        # Se si preme il tasto destro
                        if event.button == 3 and (sopra==10 or sopra==11):
                            if self.nflags < self.mine and sopra == 10:
                                self.sopra[ir][ic] = 11
                                self.nflags += 1
                            elif sopra == 11:
                                self.sopra[ir][ic] = 10
                                self.nflags -= 1
                            os_command('cancella lo schermo')
                            print('Mine rilevate: {}    |    Mine mancanti: {}'.format(self.nflags, self.mine - self.nflags))
                else:
                    self.mouse_is_there[ir][ic] = False

        # Calcolo quanti quadrati sono stati cliccati
        cliccati = sum([1 for r in self.sopra for c in r if c != 10 and c != 11])

        # Se sono uguali alla differenza tra i quadrati totali e il numero di mine si vince
        if cliccati == len(self.raws)*len(self.columns) - self.mine:        
            pg.time.delay(1000)
            self.done = True
            return 'vittoria'


    
    def borders(self, ir, ic, mode):
        """Restituisce una lista con i valori o le coordinate dei quadrati
        adiacenti al quadrato delle coordinate date;
        il parametro mode decide cosa restituire
        """
        coords = [(-1,-1), (-1,0), (-1,1),
                  (0, -1),          (0,1),
                  (1, -1), (1, 0), (1, 1)]
        if mode == 'indexes':
            return [(ir+x,ic+y) for x,y in coords
                           if 0<= ir+x < len(self.raws) and 0 <= ic+y < len(self.columns)]
        else:
            return [self.sotto[ir+x][ic+y] for x,y in coords
                           if 0 <= ir+x < len(self.raws) and 0 <= ic+y < len(self.columns)]


    def scopre(self, ir, ic):
        """Calcola se il quadrato delle coordinate date è vuoto:
        Se il quadrato in questione è una mine restituisce vero,
        invece  se è vuoto scopre il layer sopra di tutti i
        quadrati vuoti adiacenti a sè e di tutti gli altri,
        fino a quando non si incontra un numero o una mina.
        """
        if self.sotto[ir][ic] != 9:
            self.sopra[ir][ic] = self.sotto[ir][ic]
            if self.sotto[ir][ic] == 0:
                for ir2, ic2 in self.borders(ir, ic, 'indexes'):
                    if self.sopra[ir2][ic2] == 11:
                        continue
                    if self.sotto[ir2][ic2] == 0 and self.sopra[ir2][ic2] == 10:
                        self.scopre(ir2, ic2)
                    self.sopra[ir2][ic2] = self.sotto[ir2][ic2]
        else:
            return True


    def render(self, screen):
        """Per renderizzare il campo,
        Se la partita è finita si visualizza solo il secondo layer
        """
        if self.done:
            self.surfs[10].set_alpha(200)
            for ir, raw in enumerate(self.sotto):
                for ic, column in enumerate(raw):
                    screen.blit(self.surfs[column], self.rect[ir][ic])
                    if self.sotto[ir][ic] == 9:
                        screen.blit(self.surfs[self.sopra[ir][ic]], self.rect[ir][ic])
        else:              
    
            for ir, raw in enumerate(self.sopra):
                for ic, column in enumerate(raw):
                    screen.blit(self.surfs[column], self.rect[ir][ic])
                    if self.mouse_is_there[ir][ic] and self.sopra[ir][ic] >= 10:
                        s = pg.Surface(self.rect[ir][ic].size, pg.SRCALPHA)
                        pg.draw.rect(s, (255, 255, 255, 150), s.get_rect())
                        screen.blit(s, self.rect[ir][ic])
