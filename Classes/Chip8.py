import random
import pygame


class Chip8:
    ROWS = 32
    COLS = 64

    def __init__(self, display, keyboard):
        self.ram = [0] * 4096
        self.V = [0] * 16
        self.i = 0
        self.delay_timer = 0
        self.sound_timer = 0
        self.pc = 512
        self.sp = 0
        self.stack = [0] * 16
        self.scale = 15
        self.paused = False
        self.Display = display
        self.Keyboard = keyboard

    def load_rom(self, filename):
        file = open(filename, "rb").read()
        for index, byte in enumerate(file):
            self.ram[self.pc + index] = byte

    def load_sprites(self):
        sprites = [0xF0, 0x90, 0x90, 0x90, 0xF0,
                   0x20, 0x60, 0x20, 0x20, 0x70,
                   0xF0, 0x10, 0xF0, 0x80, 0xF0,
                   0xF0, 0x10, 0xF0, 0x10, 0xF0,
                   0x90, 0x90, 0xF0, 0x10, 0x10,
                   0xF0, 0x80, 0xF0, 0x10, 0xF0,
                   0xF0, 0x80, 0xF0, 0x90, 0xF0,
                   0xF0, 0x10, 0x20, 0x40, 0x40,
                   0xF0, 0x90, 0xF0, 0x90, 0xF0,
                   0xF0, 0x90, 0xF0, 0x10, 0xF0,
                   0xF0, 0x90, 0xF0, 0x90, 0x90,
                   0xE0, 0x90, 0xE0, 0x90, 0xE0,
                   0xF0, 0x80, 0x80, 0x80, 0xF0,
                   0xE0, 0x90, 0x90, 0x90, 0xE0,
                   0xF0, 0x80, 0xF0, 0x80, 0xF0,
                   0xF0, 0x80, 0xF0, 0x80, 0x80]
        for num in range(0, len(sprites)):
            self.ram[num] = sprites[num]

    def decode_execute_opcode(self, opcode):
        op = (opcode & 0xF000)
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        match op:
            case 0x0000:
                if opcode == 0x00E0:
                    self.Display.clear()
                elif opcode == 0x00EE:
                    self.pc = self.stack.pop()
                    self.sp -= 1
            case 0x1000:
                self.pc = (opcode & 0xFFF)
            case 0x2000:
                nnn = (opcode & 0xFFF)
                self.sp += 1
                self.stack.append(self.pc)
                self.pc = nnn
            case 0x3000:
                if self.V[x] == (opcode & 0xFF):
                    self.pc += 2
            case 0x4000:
                if self.V[x] != (opcode & 0xFF):
                    self.pc += 2
            case 0x5000:
                if self.V[x] == self.V[y]:
                    self.pc += 2
            case 0x6000:
                self.V[x] = (opcode & 0xFF)
            case 0x7000:
                self.V[x] = (self.V[x] + (opcode & 0xFF)) % 256
            case 0x8000:
                lastNibble = (opcode & 0xF)
                match lastNibble:
                    case 0x0:
                        self.V[x] = self.V[y]
                    case 0x1:
                        self.V[x] |= self.V[y]
                    case 0x2:
                        self.V[x] &= self.V[y]
                    case 0x3:
                        self.V[x] ^= self.V[y]
                    case 0x4:
                        self.V[x] += self.V[y]
                        if self.V[x] > 0xFF:
                            self.V[0xF] = 1
                        else:
                            self.V[0xF] = 0
                        self.V[x] &= 0xFF
                    case 0x5:
                        if self.V[x] < self.V[y]:
                            self.V[0xF] = 0
                        elif self.V[x] > self.V[y]:
                            self.V[0xF] = 1
                        self.V[x] -= self.V[y]
                        self.V[x] &= 0xFF
                    case 0x6:
                        self.V[0xF] = (self.V[x] & 0x1)
                        self.V[x] >>= 1
                    case 0x7:
                        self.V[0xF] = 0
                        if self.V[y] > self.V[x]:
                            self.V[0xF] = 1
                        self.V[x] = self.V[y] - self.V[x]
                    case 0xE:
                        self.V[0xF] = (self.V[x] & 0x80)
                        self.V[x] <<= 1

            case 0x9000:
                if self.V[x] != self.V[y]:
                    self.pc += 2
            case 0xA000:
                self.i = (opcode & 0xFFF)
            case 0xB000:
                self.pc = (opcode & 0xFFF) + self.V[0]
            case 0xC000:
                self.V[x] = random.randint(0, 255) & (opcode & 0xFF)
            case 0xD000:
                width = 8
                height = (opcode & 0xF)
                self.V[0xF] = 0
                for row in range(0, height):
                    sprite = self.ram[self.i + row]
                    for col in range(0, width):
                        if sprite & 0x80 > 0:
                            if self.Display.set_pixel(self.V[x] + col, self.V[y] + row):
                                self.V[0xF] = 1
                        sprite <<= 1

            case 0xE000:
                lastNibble = (opcode & 0xFF)
                match lastNibble:
                    case 0x9E:
                        print(self.Keyboard.is_key_pressed(self.V[x]))
                        if self.Keyboard.is_key_pressed(self.V[x]):
                            self.pc += 2
                    case 0xA1:
                        print(self.Keyboard.is_key_pressed(self.V[x]))
                        if not self.Keyboard.is_key_pressed(self.V[x]):
                            self.pc += 2
            case 0xF000:
                lastNibble = (opcode & 0xFF)
                match lastNibble:
                    case 0x07:
                        self.V[x] = self.delay_timer
                    case 0x0A:
                        print("waiting for input")
                        while True:
                            event = pygame.event.wait()
                            if event.type == pygame.KEYDOWN:
                                if event.key in self.Keyboard.keys.keys():
                                    self.Keyboard.keysPressed[event.key] = 1
                                    break
                    case 0x15:
                        self.delay_timer = self.V[x]
                    case 0x18:
                        self.sound_timer = self.V[x]
                    case 0x1E:
                        self.i += self.V[x]
                    case 0x29:
                        self.i = self.V[x] * 5
                    case 0x33:
                        self.ram[self.i] = (self.V[x] // 100)
                        self.ram[self.i + 1] = (self.V[x] % 100 // 10)
                        self.ram[self.i + 2] = (self.V[x] % 10)
                    case 0x55:
                        for num in range(x + 1):
                            self.ram[self.i + num] = self.V[num]
                    case 0x65:
                        for num in range(x + 1):
                            self.V[num] = self.ram[self.i + num]

    def update_timers(self):
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1

    def cpu_cycle(self):
        opcode = (self.ram[self.pc] << 8) | self.ram[self.pc + 1]
        self.update_timers()
        self.pc += 2
        self.decode_execute_opcode(opcode)
