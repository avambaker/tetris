class Sparkle:
    def __init__(self, x:int=0, y:int=0):
        self.x = x
        self.y = y

    # move the current block downward by one
    def move(self, horizontal, vertical)->None:
        self.x += horizontal
        self.y += vertical