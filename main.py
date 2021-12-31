from Classes.Chip8 import Chip8
from Classes.Display import Display
from Classes.Keyboard import Keyboard
import pygame
import sys
import time
display = Display()
chip8 = Chip8(display)
keyboard = Keyboard()
FPS = 60
clock = pygame.time.Clock()
chip8.load_rom('./Roms/ibm_logo.ch8')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if str(event.key) in keyboard.keys.keys():
                print(keyboard.keys[f"{event.key}"])
    chip8.cpu_cycle()
    display.render()
    pygame.display.update()
    clock.tick(FPS)
