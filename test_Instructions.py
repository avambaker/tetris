import unittest
from Instructions import Instructions

class TestGame(unittest.TestCase):
    
    def test_printStartGame(self):
        Instructions.printStartGame(['x', 'x', 'x'])
        difficulty, threshold, player_a, score, player_b, score_b = (0, 0, 'Player A', 0, 'Player B', 1)
        Instructions.printStats([difficulty, threshold, [score, score_b]])

if __name__ == '__main__':
    unittest.main()