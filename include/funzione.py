import os
import platform

def os_command(comando):
    if platform.system() == 'Linux':
        if comando == 'cancella lo schermo':
            return os.system('clear')
    if platform.system() == 'Windows':
        if comando == 'cancella lo schermo':
            return os.system('cls')

