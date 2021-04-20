import os

# nascondo il messaggio di pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

# Uso il pacchetto pygame per fare mini giochi
import pygame as pg
import sys

sys.path.append('include')
sys.path.append('src')

import campo
import text
from funzione import os_command

pg.init()

actual_w = int(pg.display.Info().current_w / 32)
actual_h = int(pg.display.Info().current_h / 32)

# All'inizio chiedo all'utente due input:
# le dimensioni della griglia e il numero di mine,
# e le richiedo fino a quando non si mette un valore corretto
while True:
    size = input('Dimensioni?')
    if size == 'schermo intero':
        print('In questo modo il campo sarà di ' + str(actual_w) + 'x' + str(actual_h) + ', premi ESC per uscire')
        break
    try:
        size = tuple(map(lambda x: abs(int(x)),size.split('x')))
        if size[0] > actual_w:
            size = (actual_w, size[1])
        if size[1] > actual_h:
            size = (size[0], actual_h)
        if len(size) < 2:
            raise ValueError
        break
    except ValueError:
        os_command('cancella lo schermo')
        print('I valori accettibili sono "lunghezzaxlarghezza" oppure "schermo intero"')

while True:
    try:
        mine = abs(int(input('Numero di mine:')))
        if size == 'schermo intero':
            if mine < actual_w * actual_h:
                break
        else:
            if mine < size[0] * size[1]:
                break
            else:
                print('Le mine devono essere minori dell\'effettivo campo')
    except ValueError:
        os_command('cancella lo schermo')
        print('Dovresti mettere un numero')


if size == 'schermo intero':
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
else:
    screen = pg.display.set_mode(tuple(map(lambda x: x*32, size)))
pg.display.set_caption('Prato fiorito')

# Creo i messaggi che vengono renderizzati in caso di perdita o vittoria
perdita = text.Text('Hai perso, che peccato', size = 30)
vittoria = text.Text('Hai vinto, complimenti!', size = 30)

# Istanzio il campo
c = campo.Campo()

# Costruisco il campo
c.build(screen, mine)

print('Mine rilevate: {}    |    Mine mancanti: {}'.format(0, mine))

clock = pg.time.Clock()

# booleano per quando si vince o si perde
finito = False

# Booleano per quando invece il giocatore smette di giocare
done = False

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
            break

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                done = True
                break

        if not finito:
            finito = c.update(event)
        elif event.type == pg.KEYDOWN:
            # Quando si finisce una partita
            # si ha la possibilità di cominciarne una nuova,
            # premendo un qualsiasi tasto
            finito = False
            c.build(screen, mine)

    c.render(screen)

    # Il colore dello sfondo di fine partita è arbitrario
    if finito == 'perdita':
        perdita.render(screen, (48, 53, 108, 200))
        os_command('cancella lo schermo')
        print('Premi un tasto qualsiasi per iniziare una nuova partita!')
    elif finito == 'vittoria':
        vittoria.render(screen, (48, 53, 108, 200))
        os_command('cancella lo schermo')
        print('Premi un tasto qualsiasi per iniziare una nuova partita!')

    pg.display.update()
    clock.tick(30)

# chiudo pygame ed esco
pg.quit()
sys.exit()
