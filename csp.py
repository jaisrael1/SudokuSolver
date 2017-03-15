from sudokuReader import SudokuReader
import copy
import sys

class manager: # Takes in the filepath, creates a CSP object for each puzzle and calls backtrack on it
    def __init__(self, filePath):
        self.puzzles = SudokuReader(filePath).puzzles
        for num, board in self.puzzles.items():
            puzzle = csp(board)
            puzzle = backTrack(puzzle)
            solved = ""
            for i in range(9):
                for j in range(9):
                    solved += puzzle.board[i][j]
            print(solved)


class csp:

    def __init__(self, board): # Creates a CSP object for a given boards, propogates initial constraints
        self.X = []
        self.D = {}
        self.C = {}
        self.board = board
        for i in range(9):
            for j in range(9):
                var = (i,j)
                self.X.append(var)
                self.C [var] = 0
                if board[i][j].isdigit():
                    init_domain = set([int(board[i][j])])
                else:
                    init_domain = set(range(1,10))
                self.D[var] = init_domain
        for i in range(9):
            for j in range(9):
                self.getConstraints((i,j))
        for known_val in [x for x in self.X if len(self.D[x]) == 1]:
            self.propogate_constraint(known_val)

    def printCSP(self): #Prints a board in a human readable format
        for i in range(9):
            for j in range(9):
                if len(self.D[i,j]) == 1:
                    val = list(self.D[i,j])[0]
                    print(val, " ", end="")
                else:
                    print(" . ", end="")
            print()

    def getConstraints(self, coord): # Gets all of the constraints for a single cell
        row = self.rowConstraints(coord)
        col = self.colConstraints(coord)
        box = self.boxConstraints(coord)
        all_constraints = row + col + box
        self.C[coord] = set(all_constraints)

    def rowConstraints(self, coord):
        this_row = []
        for var in self.X:
            if var[0] == coord[0] and var != coord:
                this_row.append(var)
        return this_row

    def colConstraints(self, coord):
        this_col = []
        for var in self.X:
            if var[1] == coord[1] and var != coord:
                this_col.append(var)
        return this_col

    def boxConstraints(self, coord):
        this_box = []
        xstart = coord[0]//3 * 3
        ystart = coord[1]//3 * 3
        for x in range(xstart, xstart + 3):
            for y in range(ystart, ystart + 3):
                if (x,y) != coord:
                    this_box.append((x,y))
        return this_box

    def propogate_constraint(self, coord): # Propogates the contraints from a single cell
        val = list(self.D[coord])[0]
        for neighbor in self.C[coord]:
             if val in self.D[neighbor]:
                self.D[neighbor].remove(val)

    def AC3(self): # AC3 algorithm, uses arc consistancy to propogate all contraints
        arcs = []
        for x in self.X:
            for y in self.C[x]:
                arcs.append((x,y))
        while arcs:
            var1, var2 = arcs.pop(0)
            if(self.revise(var1, var2)):
                if len(self.D[var1])==0:
                    return False
                for neighbor in self.C[var1]:
                    if neighbor != var2:
                        arcs.append((neighbor,var1))
        return True

    def revise(self, var1, var2): # Part of AC3, tells us if the domain changed and actually does it
        revised = False
        toRemove = []
        for x in self.D[var1]:
            satisfied = False
            for y in self.D[var2]:
                if x != y:
                    satisfied = True
            if not satisfied:
                toRemove.append(x)
                revised = True
        for q in toRemove:
            self.D[var1].remove(q)

        return revised

    def unsetVars(self): # Returns a list of all unassigned cells
        return [x for x in self.X if len(self.D[x]) > 1]

    def unassignedVar(self): # Heuristic is var with the smallest Domain first
        unsetVars = self.unsetVars()
        unsetVar = min([x for x in unsetVars], key=lambda x: len(self.D[x]))
        return unsetVar

    def orderValues(self, var):  # Returns a dictionary associating each value for a cell with the number of domain changes is causes

        dict = {}
        for val in self.D[var]:
            dict[val]=0
            for constraint in self.C[var]:
                if val in self.D[constraint]:
                    dict[val] += 1
        return dict

    def updateBoard(self): # Modifies the board state to reflect domain changes
        for coord in self.D.keys():
            if len(self.D[coord]) == 1:
                self.board[coord[0]][coord[1]] = str(list(self.D[coord])[0])

def backTrack(currentCsp): # Propogates contraints, assigns a new value, repeats. DFS search which can figure out which paths are invalid
    if len(currentCsp.unsetVars()) == 0:
        return currentCsp
    var = currentCsp.unassignedVar()
    potentialVals = currentCsp.orderValues(var)
    sortedVals = sorted(potentialVals.keys(), key=lambda x: potentialVals[x]) # Heuristic is value that causes lowest number of domain changes
    for val in sortedVals:
        board = copy.deepcopy(currentCsp.board)
        board[var[0]][var[1]] = str(val)
        clone = csp(board)
        isValid = clone.AC3()
        clone.updateBoard()
        if isValid:
            result = backTrack(clone)
            if result:
                return result
    return False


def main():
    fpath = sys.argv[1]
    manager(fpath)

manager()