from KBHit import KBHit
from Instructions import Instructions
from Disk import Disk
import time

class Game():
    def __init__(self, board):
        self.__name__ = 'Game' # name of class
        self.level, self.delay, self.threshold = (0, 1, 0)
        self.board_type = board
        self.game_board = board()
        self.kb = KBHit() # a class that read input from the keyboard
        self.disk = Disk(self.game_board.__name__ + self.__name__) # a class that saves and loads from json files
        self.game_state = True
        self.preview = False
        self.score = 0
        self.cur_high_score = 0
        self.difficulty = ['BEGINNER', 'INTERMEDIATE', 'ADVANCED']
        self.frames = []
    
    # get standard stats
    def getStats(self):
        return self.difficulty, self.threshold, self.score, self.disk.high_score, self.cur_high_score, self.preview

    # standard variable setup for a new game
    def setup(self):
        self.level, self.delay, self.threshold = Instructions.selectDifficulty()
        self.difficulty = self.difficulty[self.level]
        self.preview = Instructions.setPreview()

    # start standard game
    def run(self)->None:
        while self.game_state:
            while not self.game_board.tryDump():
                move_count = 0
                self.display()
                while self.kb.kbhit() and move_count < 3:
                    self.buttonPress()
                    move_count += 1
                    self.display()
                if self.game_state:
                    self.game_board.tryMoveDown()
                time.sleep(self.delay)
            if self.game_board.checkThreshold(self.threshold):
                self.levelLost()
            full_rows = self.game_board.cleanRows()
            if full_rows > 0:
                self.score += full_rows * self.level
        return
    
    # standard game over procedure
    def levelLost(self):
        self.game_board.dump()
        self.display()
        self.game_state = False
        print("\n\t\t\tYou lost!")
        Instructions.printStats(self.getStats())
        if self.checkScores():
            self.disk.updateHighScore(self.score)
        replay = input("\nWould you like to watch a replay of your game (y/n)?: ")
        print(replay)
        if replay == 'y':
            for frame in self.frames:
                print("\n")
                time.sleep(0.5)
                for row in frame:
                    print(row)
        restart = input("\nWould you like to play again (y/n)?: ")
        print(restart)
        if restart == 'y':
            self.newGame()
        else:
            print("Quitting game...\n")
    
    # create new game
    def newGame(self):
        self.cur_high_score = max(self.cur_high_score, self.score)
        self.score = 0
        self.game_board = self.board_type()
        self.game_state = True
    
    # check if current score beats high score
    def checkScores(self):
        if self.score > self.disk.high_score:
            return True
        else:
            return False
    
    # if a button is pressed execute the relevant task
    def buttonPress(self):
        key = self.kb.getch()
        if ord(key) == 27:
            if self.kb.getch() == "[":
                arrow_key = self.kb.getch()
                if arrow_key == 'D':
                    self.game_board.tryMoveLeft()
                    return
                elif arrow_key == 'C':
                    self.game_board.tryMoveRight()
                    return
            else:
                self.quitGame()
        elif key == 'r':
            self.game_board.tryRotate()
        elif key == 'h':
            Instructions.printHelpMenu()
            resume = input('Are you ready to resume? (y/n): ')
        elif key == 's':
            Instructions.printStats(self.getStats())
        elif key == 'p':
            self.pause()
    
    # pause game
    def pause(self):
        print("\n\t\t\t[PAUSE]")
        print("\n\tHit any key to resume the game")
        while not self.kb.kbhit():
            time.sleep(.5)
        print("\n\t\t\t[RESUME]")
        time.sleep(1)
    
    # quit game procedure
    def quitGame(self):
        self.game_state = False
        save_game = input("\nWould you like to save your progress? (y/n): ")
        print(save_game)
        if save_game == 'y':
            self.disk.saveGame(self.makeSaveDict())
        print('\nQuitting game...\n')
        quit()
    
    # save game to json
    def makeSaveDict(self):
        print('\nSaving game...')
        saved_game = dict()
        saved_game['Board'] = self.game_board.board
        saved_game['Level'] = self.level
        saved_game['Delay'] = self.delay
        saved_game['Threshold'] = self.threshold
        saved_game['Score'] = self.score
        saved_game['BlockType'] = str(self.game_board.cur_block.__class__.__name__)
        saved_game['BlockCoordinates'] = (self.game_board.cur_block.x, self.game_board.cur_block.y)
        saved_game['BlockRotation'] = self.game_board.cur_block.current_direction
        saved_game['Preview'] = self.preview
        saved_game['RoundScore'] = self.cur_high_score
        saved_game['Difficulty'] = self.difficulty
        saved_game['Frames'] = self.frames
        saved_game = self.saveExtras(saved_game)
        return saved_game
    
    # save any special objects
    def saveExtras(self, saved_game):
        return saved_game

    # save game to json
    def uploadSavedGame(self):
        saved_game = self.disk.loadSavedGame()
        self.game_board.board = saved_game['Board']
        self.level = saved_game['Level']
        self.delay = saved_game['Delay']
        self.threshold = saved_game['Threshold']
        self.score = saved_game['Score']
        type = saved_game['BlockType']
        x, y = saved_game['BlockCoordinates']
        rotation = saved_game['BlockRotation']
        self.preview = saved_game['Preview']
        self.cur_high_score = saved_game['RoundScore']
        self.difficulty = saved_game['Difficulty']
        self.frames = saved_game['Frames']
        self.game_board.setBlock(type, x, y, rotation)
        self.uploadExtras(saved_game)
        self.disk.clearSavedFile()
    
    # if there are extra features, load them
    def uploadExtras(self, saved_game):
        return
    
    # print standard board on the command line
    def display(self)->None:
        print("\n")
        print('\n\t\t\t['+ self.difficulty +']', end='')
        if self.preview: print("\t\t\t\t\t[NEXT BLOCK]\n")
        else: print("\n")
        string_board = self.game_board.toString()
        self.frames.append(string_board)
        next_block = self.game_board.next_block.getShape()
        for i in range(len(string_board)):
            if i < len(next_block) and self.preview:
                print(string_board[i],'\t\t',next_block[i])
            else:
                print(string_board[i])

class SurvivalGame(Game):
    def __init__(self, board):
        super().__init__(board)
        self.__name__ = 'Survival'
        self.timer = time.time()
        self.level = 1
        self.difficulty = str(self.level)
    
    # survival variable setup for new game
    def setup(self):
        self.preview = Instructions.setPreview()
    
    # start survival game
    def run(self)->None:
        while self.game_state:
            while not self.game_board.tryDump():
                move_count = 0
                self.display()
                while self.kb.kbhit() and move_count < 3:
                    self.buttonPress()
                    move_count += 1
                    self.display()
                if self.game_state:
                    self.game_board.tryMoveDown()
                time.sleep(self.delay)
                self.incrementTimer()
                if self.delay <= 0.05:
                    self.levelWon()
            if self.game_board.checkThreshold(self.threshold):
                self.levelLost()
            full_rows = self.game_board.cleanRows()
            if full_rows > 0:
                self.score += full_rows * 0.1
    
    # incrememnt timer
    def incrementTimer(self):
        if time.time() > (self.timer + 2):
            self.delay -= 0.05
            self.timer = time.time()
    
    # move to the next level or win game
    def levelWon(self):
        self.game_state = False
        print('\n\t\t\tYou Won!')
        Instructions.play()
        self.score += 1
        if self.checkScores():
            self.disk.updateHighScore(self.score)
        self.level += 1
        self.delay = 1 - self.level * 0.25
        Instructions.printStartGame(self.difficulty)
        Instructions.printStats([self.getStats])
        time.sleep(2)
        self.game_board = self.board_type()
        self.game_state = True
    
    # create new game
    def newGame(self):
        self.cur_high_score = max(self.cur_high_score, self.score)
        self.score = 0
        self.delay = 1
        self.game_board = self.board_type()
        self.game_state = True

class SpecialGame(Game):
    def __init__(self, board):
        super().__init__(board)
    
    # special variable set up for a new game
    def setup(self):
        self.level, self.delay, self.threshold = Instructions.selectDifficulty()
        self.difficulty = self.difficulty[self.level]
        self.preview = Instructions.setPreview()
    
    # start special game
    def run(self)->None:
        while self.game_state:
            while not self.game_board.tryDump():
                move_count = 0
                self.display()
                while self.kb.kbhit() and move_count < 3:
                    self.buttonPress()
                    move_count += 1
                    self.display()
                if self.game_state:
                    self.game_board.tryMoveDown()
                    self.game_board.tryMoveSparkle()
                time.sleep(self.delay)
            if self.game_board.checkThreshold(self.threshold):
                self.levelLost()
    
    def saveExtras(self, saved_game):
        saved_game['Sparkle'] = (self.game_board.sparkle.x, self.game_board.sparkle.y)
        return saved_game

    def uploadExtras(self, saved_game):
        (x, y) = saved_game['Sparkle']
        self.game_board.setSparkle(x, y)

class MultiPlayerGame(Game):
    def __init__(self, board):
        super().__init__(board)
        self.__name__ = 'MultiPlayer'
        self.second_board = self.board_type()
        self.player_a = ''
        self.player_b = ''
        self.score_b = 0
        self.difficulty = 'MultiPlayer'
        self.second_frames = []
    
    # multiplayer variable setup for a new game
    def setup(self):
        self.level, self.delay, self.threshold = Instructions.selectDifficulty()
        self.player_a, self.player_b = Instructions.getPlayerNames()
    
    # start multiplayer game
    def run(self)->None:
        while self.game_state:
            while not self.game_board.tryDump() and not self.second_board.tryDump():
                move_count = 0
                self.display()
                while self.kb.kbhit() and move_count < 6:
                    self.buttonPress()
                    move_count += 1
                    self.display()
                if self.game_state:
                    self.game_board.tryMoveDown()
                    self.second_board.tryMoveDown()
                time.sleep(self.delay)
            if self.game_board.checkThreshold(self.threshold):
                self.score += 1
                self.levelLost(self.player_a)
                break
            if self.second_board.checkThreshold(self.threshold):
                self.score_b += 1
                self.levelLost(self.player_b)
                break
            self.game_board.cleanRows()
            self.second_board.cleanRows()
    
    # get multiplayer stats
    def getStats(self):
        return self.difficulty, self.threshold, [self.score, self.score_b]
    
    # game over procedure
    def levelLost(self, player):
        self.game_state = False
        self.game_board.dump()
        self.second_board.dump()
        self.display()
        print("\n\n\t\t\t", player.upper(), "WINS!!!")
        Instructions.printStats(self.getStats())
        Instructions.play()
        replay = input("\nWould you like to watch a replay of your game (y/n)?: ")
        print(replay)
        if replay == 'y':
            for frame in range(len(self.frames)):
                print("\n")
                time.sleep(0.5)
                for row in range(len(self.frames[frame])):
                    print(self.frames[frame][row], "\t", self.second_frames[frame][row])
        restart = input("\nWould you like to play again (y/n)?: ")
        print(restart)
        if restart == 'y':
            self.newGame()
        else:
            print("Quitting game...\n")
    
    # create new game
    def newGame(self):
        self.second_board = self.board_type()
        self.game_board = self.board_type()
        self.game_state = True
    
    # print both boards on the command line
    def display(self)->None:
        print("\n")
        game1 = self.game_board.toString()
        game2 = self.second_board.toString()
        self.frames.append(game1)
        self.second_frames.append(game2)
        print("\t\t\t[" + self.player_a + "]\t\t\t\t\t\t\t\t[" + self.player_b + "]\n")
        for i in range(len(game1)):
                print(game2[i], "\t", game1[i])
    
    # if a button is pressed execute the relevant task
    def buttonPress(self):
        key = self.kb.getch()
        if ord(key) == 27:
            if self.kb.getch() == "[":
                arrow_key = self.kb.getch()
                if arrow_key == 'D':
                    self.game_board.tryMoveLeft()
                    return
                elif arrow_key == 'C':
                    self.game_board.tryMoveRight()
                    return
            else:
                self.quitGame()
        elif key == 'i':
            self.game_board.tryRotate()
        elif key == 'a':
            self.second_board.tryMoveLeft()
        elif key == 'd':
            self.second_board.tryMoveRight()
        elif key == 'r':
            self.second_board.tryRotate()
        elif key == 'h':
            Instructions.printHelpMenu()
            resume = input('Are you ready to resume? (y/n): ')
        elif key == 's':
            Instructions.printStats(self.getStats())
        elif key == 'p':
            Instructions.pause()
    
    # if there are extra features, save them
    def saveExtras(self, saved_game):
        saved_game['SecondBoard'] = self.second_board.board
        saved_game['SecondBlockType'] = str(self.second_board.cur_block.__class__.__name__)
        saved_game['SecondBlockCoordinates'] = (self.second_board.cur_block.x, self.second_board.cur_block.y)
        saved_game['SecondBlockRotation'] = self.second_board.cur_block.current_direction
        saved_game['PlayerA'] = self.player_a
        saved_game['PlayerB'] = self.player_b
        return saved_game

    # if there are extra features, load them
    def uploadExtras(self, saved_game):
        self.second_board.board = saved_game['SecondBoard']
        second_type = saved_game['SecondBlockType']
        second_x, second_y = saved_game['SecondBlockCoordinates']
        second_rotation = saved_game['SecondBlockRotation']
        self.second_board.setBlock(second_type, second_x, second_y, second_rotation)
        self.player_a = saved_game['PlayerA']
        self.player_b = saved_game['PlayerB']