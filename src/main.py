from classes.game import Game, SpecialGame, SurvivalGame, MultiPlayerGame
from classes.board import SparkleBoard, FreezeBoard, Board
from classes.instructions import Instructions
import os

# initialize and run the Tetris game
def main()->None:
    print("\n\n\t\tWelcome to Tetris!\n")
    mode = Instructions.selectGameMode()
    game_types = [Game(Board), SpecialGame(SparkleBoard), SpecialGame(FreezeBoard), SurvivalGame(Board), MultiPlayerGame(Board)]
    game = game_types[mode]
    if game.disk.checkSaved() and Instructions.askLoadGame():
        game.uploadSavedGame()
    else:
        game.setup()
    Instructions.printIntro()
    Instructions.printStats(game.getStats())
    Instructions.printStartGame(game.difficulty)
    game.run()
    return

if __name__ == "__main__":
    main()