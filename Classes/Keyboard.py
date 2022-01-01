class Keyboard:
    def __init__(self):
        self.keys = {
            49: 0x1,
            50: 0x2,
            51: 0x3,
            52: 0xc,
            113: 0x4,
            119: 0x5,
            101: 0x6,
            114: 0xD,
            97: 0x7,
            115: 0x8,
            100: 0x9,
            102: 0xE,
            122: 0xA,
            120: 0x0,
            99: 0xB,
            118: 0xF
        }

        self.keysPressed = {}

    def is_key_pressed(self, key):
        if key in self.keysPressed.keys():
            return True if self.keysPressed[key] else False