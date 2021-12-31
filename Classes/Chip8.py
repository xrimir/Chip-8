import random


class Chip8:
    ROWS = 32
    COLS = 64

    def __init__(self, Display):
        self.ram = [0] * 4096
        self.V = [0] * 16
        self.i = 0
        self.VF = 0
        self.delay_register = 0
        self.sound_register = 0
        self.pc = 512  # program counter
        self.sp = -1  # stack pointer
        self.stack = [0] * 16
        self.scale = 15
        self.display = [0] * (self.ROWS * self.COLS)
        self.paused = False
        self.Display = Display

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
                    self.display.clear()
                elif opcode == 0x00EE:
                    self.pc = self.stack.pop()
                    self.sp -= 1
            case 0x1000:
                nnn = (opcode & 0xFFF)
                self.pc = nnn
            case 0x2000:
                nnn = (opcode & 0xFFF)
                self.sp += 1
                self.stack.append(self.pc)
                self.pc = nnn
            case 0x3000:
                kk = (opcode & 0xFF)
                if self.V[x] == kk:
                    self.pc += 2
            case 0x4000:
                kk = (opcode & 0xFF)
                if self.V[x] != kk:
                    self.pc += 2
            case 0x5000:
                if self.V[x] == self.V[y]:
                    self.pc += 2
            case 0x6000:
                kk = (opcode & 0xFF)
                self.V[x] = kk
            case 0x7000:
                kk = (opcode & 0xFF)
                self.V[x] += kk
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
                        regSum = (self.V[x] + self.V[y])
                        self.VF = 0
                        if regSum > 0xFF:
                            self.VF = 1
                            self.V[x] = (regSum & 0xFF)
                        else:
                            self.V[x] = regSum
                    case 0x5:
                        self.VF = 0
                        if self.V[x] > self.V[y]:
                            self.VF = 1
                        self.V[x] -= self.V[y]
                    case 0x6:
                        self.VF = (self.V[x] & 0x1)
                        self.V[x] >>= 1
                    case 0x7:
                        self.VF = 0
                        if self.V[y] > self.V[x]:
                            self.VF = 1
                        self.V[x] = self.V[y] - self.V[x]
                    case 0xE:
                        self.V[x] = (self.V[x] & 0x80)
                        self.V[x] <<= 1

            case 0x9000:
                if self.V[x] != self.V[y]:
                    self.pc += 2
            case 0xA000:
                nnn = (opcode & 0xFFF)
                self.i = nnn
            case 0xB000:
                nnn = (opcode & 0xFFF)
                self.pc = nnn + self.V[0]
            case 0xC000:
                self.V[x] = random.randrange(0, 255) & (opcode & 0xFF)
            case 0xD000:
                width = 8
                height = (opcode & 0xF)
                self.VF = 0
                for row in range(0, height):
                    sprite = self.ram[self.i + row]
                    for col in range(0, width):
                        if sprite & 0x80 > 0:
                            if self.Display.set_pixel(self.V[x] + col, self.V[y] + row):
                                self.VF = 1
                        sprite <<= 1

            case 0xE000:
                lastNibble = (opcode & 0xFF)
                match lastNibble:
                    case 0x9E:
                        print("skip instruction if keyt with the value of Vx is pressed")
                    case 0xA1:
                        print("skup next intruction if key with the value of Vx is pressed")
            case 0xF000:
                lastNibble = (opcode & 0xFF)
                match lastNibble:
                    case 0x07:
                        pass
                    case 0x0A:
                        pass
                    case 0x15:
                        pass
                    case 0x18:
                        pass
                    case 0x1E:
                        pass
                    case 0x29:
                        pass
                    case 0x33:
                        pass
                    case 0x55:
                        pass
                    case 0x65:
                        pass

        return hex(opcode)

    def execute_opcode(self):
        pass

    def cpu_cycle(self):
        opcode = self.ram[self.pc] << 8 | self.ram[self.pc + 1]
        self.pc += 2
        decoded_opcode = self.decode_execute_opcode(opcode)
        return True
