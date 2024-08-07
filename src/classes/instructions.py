import time
import os
#from classes.KBHit import KBHit as kb

class Instructions:
    
    # create help menu
    @staticmethod
    def printHelpMenu():
        keys = ['h', 'r', '<-', '->', 'esc x2', 's']
        codes = ['help menu', 'rotate block', 'move left', 'move right', 'exit', 'stats']
        print('\n\n\t\t\t[DIRECTIONS]\n')
        for i in range(len(keys)):
            tabs = 4
            if len(keys[i]) > 1: tabs -= 1
            print("key:", keys[i], "\t"*tabs, "action:", codes[i])
    
    # print intro
    @staticmethod
    def printIntro():
        print("\n\n\t**Press the 'h' key for the help menu**")
        print("\n\t**Press the 'p' key to pause**")
        print("\n\t**Double press 'esc' to exit**")
        time.sleep(2)
    
    # change the speed of the game
    @staticmethod
    def selectDifficulty():
        difficulties = ['BEGINNER', 'INTERMEDIATE', 'ADVANCED']
        print('\n')
        for i in range(len(difficulties)):
            print('[' + str(i + 1) + ']', difficulties[i])
        answer = input('\nEnter the number of the difficulty you would like: ')
        print(answer)
        try:
            level = int(answer)
            if level not in range(1, 4):
                print("\nCouldn't read input, defaulted to 'Beginner'")
                level = 1
        except:
            level = 1
            print("\nCouldn't read input, defaulted to 'Beginner'")
        if level == 1: return (0, 1, 0)
        elif level == 2: return (1, 0.75, 2)
        elif level == 3: return (2, 0.5, 4)
    
    # set preview
    @staticmethod
    def setPreview():
        turn_on_preview = input('\nWould you like to see previews of the next block? (y/n): ')
        print(turn_on_preview)
        if turn_on_preview == 'y':
            return True
        else:
            return False
    
    # print standard stats
    @staticmethod
    def printStats(vals):
        stats = ['Difficulty:', 'Threshold:', 'Current Score:', 'Your High Score:', 'Highest Score:', 'Show Preview:']
        print('\n\t\t\t[GAME STATS]')
        for i in range(len(vals)):
            print(stats[i], vals[i])
    
    # print start game
    @staticmethod
    def printStartGame(difficulty):
        time.sleep(2)
        print("\nStarting game...\n")
        print("\t\t\t[" + str(difficulty) + ']')
    
    # select which kind of game to play
    @staticmethod
    def selectGameMode():
        game_modes = ['STANDARD', 'SPARKLE', 'FREEZE', 'SURVIVAL', 'MULTIPLAYER']
        for i in range(len(game_modes)):
            print('[' + str(i + 1) + ']', game_modes[i])
        mode = input("\nSelect the number of which game mode you would like to play: ")
        print(mode)
        try:
            level = int(mode) - 1
            if level not in range(len(game_modes)):
                print("Your input could not be read. Defaulting to standard.")
                return 0
            else:
                return level
        except:
            print("Your input could not be read. Defaulting to standard.")
            return 0
    
    # ask the user if they want to play the saved game
    @staticmethod
    def askLoadGame():
        print("\nIt looks like there is a saved game!")
        print('\nWould you like to resume the previous game?')
        load_game = input("\nAnswer (y/n): ")
        print(load_game)
        if load_game == 'y':
            return True
        else:
            return False  
    
    # get collect names, return as a tuple
    @staticmethod
    def getPlayerNames():
        player_a = input("\nEnter the first player's name: ")
        print(player_a)
        player_b = input("\nEnter the second player's name: ")
        print(player_b)
        return (player_a, player_b)
    
    @staticmethod
    def play():
        file = 'sounds/win.mp3'
        os.system("afplay " + file)