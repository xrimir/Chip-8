import pygame


class Display:
    COLS = 64
    ROWS = 32

    def __init__(self):
        self.scale = 15
        self.display_width = self.ROWS * self.scale
        self.display_height = self.COLS * self.scale
        self.display = [0] * (self.ROWS * self.COLS)
        self.screen = pygame.display.set_mode((self.COLS * self.scale, self.ROWS * self.scale))

    def set_pixel(self, x, y):
        if x > self.COLS:
            x -= self.COLS
        elif x < 0:
            x += self.COLS

        if y > self.ROWS:
            y -= self.ROWS
        elif x < 0:
            y += self.ROWS

        pixelLocation = x + (y * self.COLS)
        self.display[pixelLocation] ^= 1
        return not self.display[pixelLocation]

    def render(self):
        self.screen.fill((0, 0, 0))
        for num in range(self.ROWS * self.COLS):
            x = (num % self.COLS) * self.scale
            y = (num // self.COLS) * self.scale

            if self.display[num]:
                pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(x, y, self.scale, self.scale))
        pygame.display.update()

    def clear(self):
        self.display = [0] * (self.ROWS * self.COLS)
