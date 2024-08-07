from abc import ABC
class _Block(ABC):
    def __init__(self, x:int=0, y:int=0):
        self.x = x
        self.y = y
        self.current_direction = 0
    
    # rotate the current block counterclockwise by 90 degrees
    def rotateLeft(self)->None:
        if self.current_direction == 3:
            self.setDirection(0)
        else:
            self.setDirection(self.current_direction + 1)
    
    # set the direction to the specified int
    def setDirection(self, direction):
        self.current_direction = direction
    
    # move the current block downward by one
    def moveDown(self)->None:
        self.y += 1
    
    # move the current block rightward by one
    def moveRight(self)->None:
        self.x += 1
    
    # move the current block leftward by one 
    def moveLeft(self)->None:
        self.x -= 1
    
    # return current shape of the block
    def getShape(self)->"list[list[int]]":
        return self.shapes[self.current_direction]
    
    # return the length and width of the current shape
    def getDimensions(self):
        return (len(self.shapes[self.current_direction]), len(self.shapes[self.current_direction][0]))
    
    # return the max valid x and y coordinates for the block
    def getMaxCoordinates(self):
        cur_shape = self.getShape()
        y_max = 16 - len(cur_shape)
        x_max = 21 - len(cur_shape[0])
        return (y_max, x_max)

class LBlock(_Block):
    def __init__(self, x:int=0, y:int=0):
        super().__init__(x, y)
        self.shapes = \
            [[[1, 0,],
             [1, 0,],
             [1, 0,],
             [1, 1]],

             [[0, 0, 0, 1],
             [1, 1, 1, 1]],
             
             [[1, 1],
             [0, 1],
             [0, 1],
             [0, 1]],

             [[1, 1, 1, 1],
             [1, 0, 0, 0]]]

class JBlock(_Block):
    def __init__(self, x:int=0, y:int=0):
        super().__init__(x, y)
        self.shapes = \
            [[[0, 1],
             [0, 1],
             [0, 1],
             [1, 1]],

             [[1, 0, 0, 0],
             [1, 1, 1, 1]],
             
             [[1, 1],
             [1, 0],
             [1, 0],
             [1, 0]],

             [[1, 1, 1, 1],
             [0, 0, 0, 1]]]

class OBlock(_Block):
    def __init__(self, x:int=0, y:int=0):
        super().__init__(x, y)
        self.shapes = \
            [[[1, 1,],
              [1, 1]],

             [[1, 1],
              [1, 1]],
             
             [[1, 1],
              [1, 1]],

             [[1, 1],
              [1, 1]]]

class IBlock(_Block):
    def __init__(self, x:int=0, y:int=0):
        super().__init__(x, y)
        self.shapes = \
            [[[1],
              [1],
              [1],
              [1]],

             [[1, 1, 1, 1]],
             
             [[1],
              [1],
              [1],
              [1]],

             [[1, 1, 1, 1]]]

class ZBlock(_Block):
    def __init__(self, x:int=0, y:int=0):
        super().__init__(x, y)
        self.shapes = \
            [[[0, 1],
              [1, 1],
              [1, 0]],

             [[1, 1, 0],
              [0, 1, 1]],
             
             [[0, 1],
              [1, 1],
              [1, 0]],

             [[1, 1, 0],
              [0, 1, 1]]]

class TBlock(_Block):
    def __init__(self, x:int=0, y:int=0):
        super().__init__(x, y)
        self.shapes = \
            [[[1, 0],
              [1, 1],
              [1, 0]],

             [[1, 1, 1],
              [0, 1, 0]],
             
             [[0, 1],
              [1, 1],
              [0, 1]],

             [[0, 1, 0],
              [1, 1, 1]]]

class SBlock(_Block):
    def __init__(self, x:int=0, y:int=0):
        super().__init__(x, y)
        self.shapes = \
            [[[1, 0],
              [1, 1],
              [0, 1]],

             [[0, 1, 1],
              [1, 1, 0]],
             
             [[1, 0],
              [1, 1],
              [0, 1]],

             [[0, 1, 1],
              [1, 1, 0]]]