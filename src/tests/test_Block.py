import unittest
from classes.block import LBlock, JBlock, OBlock, IBlock, ZBlock, TBlock, SBlock

class TestBlock(unittest.TestCase):
    
    def test_moveDown(self):
        block = LBlock()
        self.assertEqual(block.x, 0)
        self.assertEqual(block.y, 0)
        block.moveDown()
        self.assertEqual(block.y, 1)
        self.assertEqual(block.x, 0)
    
    def test_moveRight(self):
        block = LBlock()
        self.assertEqual(block.x, 0)
        self.assertEqual(block.y, 0)
        block.moveRight()
        self.assertEqual(block.y, 0)
        self.assertEqual(block.x, 1)
    
    def test_moveLeft(self):
        block = LBlock()
        self.assertEqual(block.x, 0)
        self.assertEqual(block.y, 0)
        block.moveLeft()
        self.assertEqual(block.y, 0)
        self.assertEqual(block.x, -1)
    
    def test_getMaxCoordinates(self):
        block = LBlock()
        for i in range(5):
            coordinate_set = (14, 17)
            if i % 2 == 0: coordinate_set = (12, 19)
            self.assertEqual(block.getMaxCoordinates(), (coordinate_set[0], coordinate_set[1]))
            block.rotateLeft()
        
if __name__ == '__main__':
    unittest.main()
