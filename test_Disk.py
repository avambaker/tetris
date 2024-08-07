import unittest
from Disk import Disk

class TestBoard(unittest.TestCase):

    def test_highScore(self):
        disk = Disk('FreezeGame')
        self.assertEqual(disk.getHighScore(), 0)
        disk.updateHighScore(1)
        self.assertEqual(disk.getHighScore(), 1)
        disk.updateHighScore(0)





if __name__ == '__main__':
    unittest.main()
