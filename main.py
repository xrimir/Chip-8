from Classes.Chip8 import Chip8
from Classes.Display import Display
from Classes.Keyboard import Keyboard
import pygame
import sys

display = Display()
keyboard = Keyboard()
chip8 = Chip8(display, keyboard)
chip8.load_sprites()
FPS = 260
clock = pygame.time.Clock()
chip8.load_rom('./Roms/pong.rom')
while True:
    chip8.cpu_cycle()
    display.render()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key in keyboard.keys.keys():
                chip8.Keyboard.keysPressed[chip8.Keyboard.keys[event.key]] = 1
        if event.type == pygame.KEYUP:
            if event.key in keyboard.keys.keys():
                chip8.Keyboard.keysPressed[chip8.Keyboard.keys[event.key]] = 0
    clock.tick(FPS)