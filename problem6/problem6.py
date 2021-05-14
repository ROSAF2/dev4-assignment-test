from random import shuffle

class Balls:
    def __init__(self):
        self._ballsNumber = 75 # number of balls
        self._balls = None

    @property
    def balls(self):
        return self._balls 
            
    def generateBalls(self): # 75 balls
        """ Creates ball combinations and stores them into a list of lists [[],[],[],[],[]] """
        letters = ['B','I','N','G','O']
        numberOfBallsForOneLetter = self._ballsNumber // len(letters) # 15 numbers for each letter
        balls = list()
        combination = None
        for i in range(self._ballsNumber):
            if i % 15 == 0: # Append new empty list for each letter in letters
                balls.append(list())
            combination = letters[i//numberOfBallsForOneLetter] + str(i + 1) # Concatenates letter and number
            balls[i//15].append(combination) # Appends combination to respective inner Ball List
        return balls

    def mixBalls(self):
        """ Returns a list with all the ball combinations but mixed """
        balls = self.generateBalls()
        # Extract balls
        allBalls = [ balls[i][j] for j in range(len(balls[0])) for i in range(len(balls)) ]
        shuffle(allBalls)
        return allBalls

class Card:
    def __init__(self):
        self._rows = 5
        self._cols = 5
        self._middleCell = (2,2)
        self._cells = self.generateCells() # list of list of individual cells
        
    @property
    def rows(self):
        return self._rows 

    @property
    def cols(self):
        return self._cols

    @property
    def cells(self):
        return self._cells 

    @cells.setter # for debugging
    def cells(self,cells):
        self._cells = cells

    def generateCells(self):
        """ Fills with random combinations each cell in the card, returns a "list of lists" """
        balls = Balls().generateBalls() # Get all the balls, the list has this structure [[],[],[],[],[]]
        cells = list()
        for k in range(len(balls)): # 75 times
            innerCells = list()
            randomizedList = balls[k] # First list in balls saved in the randomizedList variable
            shuffle(randomizedList) # shuffle the elements of the randomizedList list
            # Take first 5 random items, this will be the rows
            for i in range(self._rows): 
                if k == self._middleCell[0] and i == self._middleCell[1]: # Set middle cell to True, in a 5 x 5 grid the middle cell is at the 3rd row and 3rd column
                    innerCells.append({None: True})
                else:
                    innerCells.append({randomizedList[i]: False})
            cells.append(innerCells)
        return cells

class WinChecker:

    @staticmethod
    def checkForWin(card):
        results = list()
        results.append(WinChecker.checkColumns(card))
        results.append(WinChecker.checkRows(card))
        results.append(WinChecker.checkDiagonalOne(card))
        results.append(WinChecker.checkDiagonalTwo(card))
        if True in results: # if this is true it means that at least one of the above evaluations was true and we have a winner
            return True
        return False
    
    @staticmethod
    def checkColumns(card):
        """ Checks if all the cells in a column are equal to True """
        for combinationList in card.cells: # combinationList is a column in a card
            columnValues = [ cell[list(cell)[0]] for cell in combinationList ] # Makes a list of the values of each column/combinationList
            if False not in columnValues: # if False is not in columnValues that means all values are true, then we have a winner
                return True
        return False
    
    @staticmethod
    def checkRows(card):
        """ Check if any of the rows has all cells equal to True """
        for i in range(card.rows):
            rowValues = list()
            for j in range(card.cols):
                key = list(card.cells[j][i])[0] # key of the dictionary in the position i inside combinationList 
                value = card.cells[j][i][key]
                rowValues.append(value)
            if False not in rowValues: # if False is not in rowValues that means all values are true, then we have a winner
                return True
        return False   

    @staticmethod
    def checkDiagonalOne(card):
        """ Returns True if the diagonal from with coordenates (1,1) to (5,5) has all cells equal to True """
        diagonalValues = list()
        for i in range(card.rows):
            for j in range(card.cols):
                if i == j:
                    key = list(card.cells[j][i])[0]
                    value = card.cells[j][i][key]
                    diagonalValues.append(value)
        if False not in diagonalValues: # if False is not in diagonalValues that means all values are true, then we have a winner
            return True
        return False 

    @staticmethod
    def checkDiagonalTwo(card): 
        """ Returns True if the diagonal from with coordenates (5,1) to (1,5) has all cells equal to True """
        diagonalValues = list()
        for i in range((card.rows - 1), (0 - 1), -1): # i from 4 to 0 (decrement)
            for j in range(card.cols):
                if ((card.rows - 1) - i) == j:
                    key = list(card.cells[j][i])[0]
                    value = card.cells[j][i][key]
                    diagonalValues.append(value)
        if False not in diagonalValues: # if False is not in diagonalValues that means all values are true, then we have a winner
            return True
        return False 


class Player:
    def __init__(self,id):
        self._id = id
        self._card = Card()

    @property
    def card(self):
        return self._card 
    
    @property
    def id(self):
        return self._id 
    
    @id.setter
    def id(self,id):
        self._id = id

    
    def lookForMatchingCell(self,pickedBall): 
        """ Checks if the card contains a cell that matches the value of the pickedBall """
        for column in self._card.cells:
            for cell in column: # cell is a dictionary in this context
                key = list(cell)[0]
                if key == pickedBall: 
                    cell[key] = True
                    return True
        return False

    def checkForWin(self,pickedBall):
        """ Player checks if they have a winning pattern """
        if self.lookForMatchingCell(pickedBall):
            return WinChecker.checkForWin(self._card) # checks for a winning pattern
        return False

    def displayResults(self):
        rowsNumber = len(self._card.cells[0])
        transpose = [ [ row[i] for row in self._card.cells ] for i in range(rowsNumber) ]
        for row in transpose:
            for element in row:
                print(element, end="  ")
            print('\n')




    
class Caller:
    def __init__(self):
        self._players = set()
        self._gameBalls = Balls()

    @property
    def players(self):
        return self._players 

    @property
    def gameBalls(self):
        return self._gameBalls 

    def register(self, player):
        self._players.add(player)

    def unregister(self, player):
        self._players.discard(player) # removes player from list
    
    def notify(self,pickedBall):
        for player in self._players:
            if player.checkForWin(pickedBall): # if player has won
                return [True, f'Player {player.id} has won']
        return [False, f"No one hasn't won yet"]
            

def main():
    caller = Caller()

    # Players Registry
    nPlayers = 5
    for i in range(nPlayers):
        caller.register(Player(i+1))

    # Display players
    print(caller.players)

    # caller mixes the balls
    balls = caller.gameBalls.mixBalls()

    # Start of the game
    round = 0
    for pickedBall in balls:
        round += 1
        # caller picks a ball and notifies players
        feedback = caller.notify(pickedBall)

        # Display round results
        print(f'Round {round} Results <---\n')
        for player in caller.players:
            print(f'Player: {player.id} ' + '-'*65)
            player.displayResults()
            print()
        
        # Check feedback, game ends in case someone wins
        if feedback[0]:
            print(feedback[1])
            break

if __name__ == '__main__':
    main()