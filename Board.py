import random
import time
import os
from Instructions import Instructions
from Block import LBlock, JBlock, OBlock, IBlock, ZBlock, TBlock, SBlock
from Sparkle import Sparkle

class Board:
    def __init__(self):
        self.__name__ = 'Standard'
        self.cur_block = self.getRandomBlock()
        self.next_block = self.getRandomBlock()
        self.board = [[0] * 20 for _ in range(15)]
    
    # return a randomly shaped block
    def getRandomBlock(self):
        block_shapes = [LBlock, JBlock, OBlock, IBlock, ZBlock, TBlock, SBlock]
        return block_shapes[random.randint(0,6)](9, 0)
    
    def setBlock(self, type, x, y, rotation):
        block_names = ['LBlock', 'JBlock', 'OBlock', 'IBlock', 'ZBlock', 'TBlock', 'SBlock']
        block_shapes = [LBlock, JBlock, OBlock, IBlock, ZBlock, TBlock, SBlock]
        temp = block_shapes[block_names.index(type)](x, y)
        temp.current_direction = rotation
        self.cur_block = temp

    # check if current block is valid
    def isBlockValid(self, x:int, y:int)->bool:
        y_max, x_max = self.cur_block.getMaxCoordinates()
        if y >= y_max or y < 0 or x < 0 or x >= x_max: # check if block in boundaries
            return False
        shape = self.cur_block.getShape()
        length, width = self.cur_block.getDimensions()
        for row in range(length):
            for cell in range(width):
                if shape[row][cell] == 1:
                    if self.board[row + y][cell + x] == 1: # check if block is present
                        return False
        else:
            return True
    
    # move the block downward by 1 positon if the move is valid, otherwise do nothing 
    def tryMoveDown(self)->None:
        if self.isBlockValid(self.cur_block.x, self.cur_block.y + 1):
            self.cur_block.moveDown()
    
    # move the block downward by 1 positon if the move is valid, otherwise do nothing 
    def tryMoveRight(self)->None:
        if self.isBlockValid(self.cur_block.x + 1, self.cur_block.y):
            self.cur_block.moveRight()
    
    # move the block downward by 1 positon if the move is valid, otherwise do nothing 
    def tryMoveLeft(self)->None:
        if self.isBlockValid(self.cur_block.x - 1, self.cur_block.y):
            self.cur_block.moveLeft()
    
    # check if the block can be dumped and return results
    def tryDump(self):
        if self.isBlockValid(self.cur_block.x, self.cur_block.y + 1) == False:
            self.dump()
            self.putNewBlock()
            return True
        return False
    
    # check if the block can be rotated
    def tryRotate(self):
        original_direction = self.cur_block.current_direction
        self.cur_block.rotateLeft()
        if not self.isBlockValid(self.cur_block.x, self.cur_block.y):
            self.cur_block.setDirection(original_direction)
    
    # write current shape to the board permanently
    def dump(self)->None:
        cur_shape = self.cur_block.getShape()
        length, width = self.cur_block.getDimensions()
        for row in range(length):
            for cell in range(width):
                if cur_shape[row][cell] == 1:
                    self.board[self.cur_block.y + row][self.cur_block.x + cell] = 1
    
    # check if there is a block above the threshold
    def checkThreshold(self, threshold):
        if 1 in self.board[threshold]: return True
        else: return False

    
    # return index of full rows
    def getFullRows(self):
        full_rows = []
        for row in range(len(self.board)):
            if 0 not in self.board[row]:
                full_rows.append(row)
        return full_rows
    
    # delete full rows and replace with top space
    def cleanRows(self):
        full_rows = self.getFullRows()
        new_board = [[0] * 20 for _ in range(len(full_rows))]
        for row in range(len(self.board)):
            if row not in full_rows:
                new_board.append(self.board[row])
        self.board = new_board
        return len(full_rows)

    # put a new block on the top of the board
    def putNewBlock(self)->None:
        self.cur_block = self.next_block
        self.next_block = self.getRandomBlock()
    
    # return the current board with block on it 
    def toString(self)->str:
        tmp = [self.board[i][:] for i in range(15)]
        x = self.cur_block.x
        y = self.cur_block.y
        cur_shape = self.cur_block.getShape()
        length, width = self.cur_block.getDimensions()
        for i in range(length):
            for j in range(width):
                if y + i < 15 and x + j < 20 and x + j >= 0 and cur_shape[i][j] == 1:
                    tmp[y + i][x + j] = cur_shape[i][j]
        return tmp


class SparkleBoard(Board):
    def __init__(self):
        super().__init__()
        self.__name__ = 'Sparkle'
        self.sparkle = Sparkle(random.randint(0, 19), random.randint(0, 14))
    
    # set new sparkle
    def setSparkle(self, x, y):
        self.sparkle = Sparkle(x, y)

    # check if sparkle position would be valid
    def isSparkleValid(self, x, y):
        if y < 0 or y > 14:
            return False
        if x < 0 or x > 19:
            return False
        else:
            return True

    # check if sparkle will hit anything
    def isSparkleHit(self):
        x = self.sparkle.x
        y = self.sparkle.y
        if self.board[y][x] == 1:
            return 1
        block_length, block_width = self.cur_block.getDimensions()
        block_x = self.cur_block.x
        block_y = self.cur_block.y
        if x in range(block_x, block_x + block_length + 1) and y in range(block_y, block_y + block_width + 1):
            return 2
        else:
            return 0
    
    # try to move the sparkle in a random direction
    def tryMoveSparkle(self):
        h_move = random.randint(-1, 1)
        v_move = random.randint(-1, 1)
        x = self.sparkle.x + h_move
        y = self.sparkle.y + v_move
        if self.isSparkleValid(x, y):
            self.sparkle.move(h_move, v_move)
            hit = self.isSparkleHit()
            if hit == 1:
                self.explodeBoard(self.sparkle.x, self.sparkle.y)
            elif hit == 2:
                self.explodeBlock()
    
    # create a square on the board
    def makeSquare(self, x, y, width, c):
        for row in range(y - width, y + width + 1):
                for cell in range(x - width, x + width + 1):
                    if row in range(len(self.board)) and cell in range(len(self.board[0])):
                        self.board[row][cell] = c

    # show the block as exploded and remove it
    def explodeBlock(self):
        print("\n")
        [print(row) for row in self.toExplodedString()]
        time.sleep(1)
        self.putNewBlock()

    # remove a square around the sparkle
    def explodeBoard(self, x, y):
        self.makeSquare(x, y, 1, '*')
        print("\n")
        [print(row) for row in self.toString()]
        time.sleep(1)
        self.makeSquare(x, y, 1, 0)
        print("\n")
        [print(row) for row in self.toString()]
        time.sleep(1)
    
    # return the current board with block and sparkle on it
    def toString(self)->str:
        tmp = [self.board[i][:] for i in range(15)]
        x = self.cur_block.x
        y = self.cur_block.y
        cur_shape = self.cur_block.getShape()
        length, width = self.cur_block.getDimensions()
        for i in range(length):
            for j in range(width):
                if y + i < 15 and x + j < 20 and x + j >= 0:
                    if cur_shape[i][j] == 1:
                        tmp[y + i][x + j] = 1
        tmp[self.sparkle.y][self.sparkle.x] = '*'
                    
        return tmp

    # return the current board with the block exploded
    def toExplodedString(self)->str:
        tmp = [self.board[i][:] for i in range(15)]
        x = self.cur_block.x
        y = self.cur_block.y
        cur_shape = self.cur_block.getShape()
        length, width = self.cur_block.getDimensions()
        for i in range(length):
            for j in range(width):
                if y + i < 15 and x + j < 20 and x + j >= 0:
                    if cur_shape[i][j] == 1:
                        tmp[y + i][x + j] = '*'
        tmp[self.sparkle.y][self.sparkle.x] = '*'
                    
        return tmp

class FreezeBoard(Board):
    def __init__(self):
        super().__init__()
        self.__name__ = 'Freeze'
        self.sparkle = Sparkle(random.randint(0, 19), random.randint(8, 14))
        self.threshold = 0
    
    # set new sparkle
    def setSparkle(self, x, y):
        self.sparkle = Sparkle(x, y)

    # return the current board with block and sparkle on it
    def toString(self)->str:
        tmp = [self.board[i][:] for i in range(15)]
        x = self.cur_block.x
        y = self.cur_block.y
        cur_shape = self.cur_block.getShape()
        length, width = self.cur_block.getDimensions()
        for i in range(length):
            for j in range(width):
                if y + i < 15 and x + j < 20 and x + j >= 0:
                    if cur_shape[i][j] == 1:
                        tmp[y + i][x + j] = 2
            tmp[self.sparkle.y][self.sparkle.x] = '+'
                    
        return tmp
    
    # check if sparkle position would be valid
    def isSparkleValid(self, x, y):
        if y < 8 or y > 14:
            return False
        if x < 0 or x > 19:
            return False
        if self.board[y][x] == 1:
            return False
        else:
            return True

    # check if sparkle hit the current block
    def isSparkleHit(self):
        x = self.sparkle.x
        y = self.sparkle.y
        block_length, block_width = self.cur_block.getDimensions()
        block_x = self.cur_block.x
        block_y = self.cur_block.y
        if x in range(block_x, block_x + block_length + 1) and y in range(block_y, block_y + block_width + 1):
            return True
        else:
            return False
    
    # try to move the sparkle in a random direction
    def tryMoveSparkle(self):
        h_move = random.randint(-1, 1)
        v_move = random.randint(-1, 1)
        x = self.sparkle.x + h_move
        y = self.sparkle.y + v_move
        if self.isSparkleValid(x, y):
            self.sparkle.move(h_move, v_move)
            if self.isSparkleHit():
                self.dump()