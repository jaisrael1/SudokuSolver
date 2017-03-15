

class SudokuReader: # Reads in a file and creates a set of data structures to represent the boards

    def __init__(self, filePath):
        self.filePath = filePath
        self.puzzles = {}
        with open(self.filePath, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                board = []
                for j in range(9):
                    tempRow = []
                    for j in range(9):
                        tempRow.append(0)
                    board.append(tempRow)
                line = line[:-1]
                rows = [line[q:q + 9] for q in range(0, len(line), 9)]
                for x,r in enumerate(rows):
                    for a,b in enumerate(list(r)):
                        board[x][a] = b
                self.puzzles[i] = board