import unittest
from classes.game import Game, SpecialGame, MultiPlayerGame, SurvivalGame
from classes.board import Board, SparkleBoard, FreezeBoard
import json

class TestGame(unittest.TestCase):
    
    def test_updateHighScoreSpecial(self):
        for mode in [Game(Board), SpecialGame(SparkleBoard), SpecialGame(FreezeBoard)]:
            game = mode
            #print(mode.__name__, game.getKey())
            game.score = game.high_score + 1
            orig_score = game.high_score
            game.updateHighScore()
            with open('HighScores.json') as check:
                json_score = json.load(check)[game.getKey()]
                self.assertEqual(json_score, game.score)
                self.assertEqual(json_score, game.high_score)
                self.assertNotEqual(json_score, orig_score)
    
    def resetScores(self):
        with open('HighScores.json', 'r+') as f:
            json_scores = json.load(f)
            print(json_scores)
            f.seek(0)
            for key in json_scores:
                json_scores[key] = json_scores[key] - 1
            json.dump(json_scores, f)
    
    def test_standardDifficulty(self):
        game_board = Game(Board)
        print(game_board.difficulty)
    
    def test_printStats(self):
        standard_game = Game(Board)
        self.assertEqual(standard_game.getStats(), ('BEGINNER', 0, False, 0, standard_game.high_score))
        multiplayer_game = MultiPlayerGame(Board)
        self.assertEqual(multiplayer_game.getStats(), ('MultiPlayer', 0))
    
    def test_printStartGame(self):
        standard_game = Game(Board)
        standard_game.instructions.printStats(standard_game.getStats())
        standard_game.instructions.printStartGame(standard_game.getStats())


if __name__ == '__main__':
    unittest.main()
