import json

class Disk():
    def __init__(self, KEY):
        self.KEY = KEY
        self.SAVE_KEY = 'session_data/Saved' + self.KEY + '.json'
        self.high_score = self.getHighScore()

    def getHighScore(self):
        with open('session_data/HighScores.json', 'r') as f:
            return json.load(f)[self.KEY]
    
    # check if there is a saved game of this type
    def checkSaved(self):
        with open(self.SAVE_KEY, 'r') as f:
            saved = json.load(f)
            if len(saved.keys()) > 0:
                return True
        return False
    
    # clear json dict in file
    def clearSavedFile(self):
        with open(self.SAVE_KEY, 'w') as file:
            file.write('{}')
    
    # save game to json file
    def saveGame(self, game):
        with open(self.SAVE_KEY, 'w') as file:
            json.dump(game, file)
            print('Game saved successfully.')
    
    # update high score
    def updateHighScore(self, score):
        self.high_score = score
        print('\n\t\t\tNew High Score!')
        with open('session_data/HighScores.json', 'r+') as file:
            high_scores = json.load(file)
            file.seek(0)
            high_scores[self.KEY] = score
            json.dump(high_scores, file)
    
    # write items from json to dict
    def loadSavedGame(self):
        print('\nLoading game...')
        with open(self.SAVE_KEY, 'r+') as file:
            return json.load(file)