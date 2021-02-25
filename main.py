#!/usr/bin/env python
import struct, string, math


class SudokuBoard:
    """The sudoku board game object the player will manipulate."""
  
    def __init__(self, size, board):
        """the constructor for the SudokuBoard"""
        self.BoardSize = size #the size of the board
        self.CurrentGameBoard = board #the current state of the game board
        self.BoardChecker = [[[True for x in range(size)] for x in range(size)] for x in range (size*size)] #initialize 3D checker array

    def set_value(self, row, col, value):
        """This function will create a new sudoku board object with the input
        value placed on the GameBoard row and col are both zero-indexed"""
        self.CurrentGameBoard[row][col]=value
        return SudokuBoard(self.BoardSize, self.CurrentGameBoard)
                                                                  
    def print_board(self):
        """Prints the current game board. Leaves unassigned spots blank."""
        div = int(math.sqrt(self.BoardSize))
        dash = ""
        space = ""
        line = "+"
        sep = "|"
        for i in range(div):
            dash += "----"
            space += "    "
        for i in range(div):
            line += dash + "+"
            sep += space + "|"
        for i in range(-1, self.BoardSize):
            if i != -1:
                print "|",
                for j in range(self.BoardSize):
                    if self.CurrentGameBoard[i][j] > 9:
                        print self.CurrentGameBoard[i][j],
                    elif self.CurrentGameBoard[i][j] > 0:
                        print "", self.CurrentGameBoard[i][j],
                    else:
                        print "  ",
                    if (j+1 != self.BoardSize):
                        if ((j+1)//div != j/div):
                            print "|",
                        else:
                            print "",
                    else:
                        print "|"
            if ((i+1)//div != i/div):
                print line
            else:
                print sep

def parse_file(filename):
    """Parses a sudoku text file into a BoardSize, and a 2d array which holds
    the value of each cell. Array elements holding a 0 are considered to be
    empty."""

    f = open(filename, 'r')
    BoardSize = int( f.readline())
    NumVals = int(f.readline())

    #initialize a blank board
    board= [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

    #populate the board with initial values
    for i in range(NumVals):
        line = f.readline()
        chars = line.split()
        row = int(chars[0])
        col = int(chars[1])
        val = int(chars[2])
        board[row-1][col-1]=val
    
    return board
    
def is_complete(sudoku_board):
    """Takes in a sudoku board and tests to see if it has been filled in
    correctly."""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    #check each cell on the board for a 0, or if the value of the cell
    #is present elsewhere within the same row, column, or square
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col]==0: #0 means empty space
                return False
            for i in range(size):
                if ((BoardArray[row][i] == BoardArray[row][col]) and i != col): #duplicate numbers in same row
                    return False
                if ((BoardArray[i][col] == BoardArray[row][col]) and i != row): #dupliacte numbers in same column
                    return False
            #determine which square the cell is in
            SquareRow = row // subsquare
            SquareCol = col // subsquare
            for i in range(subsquare):
                for j in range(subsquare):
                    if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                         == BoardArray[row][col]) #if there are any duplicates in the subsquare
                        and (SquareRow*subsquare + i != row) #and not the same row #
                        and (SquareCol*subsquare + j != col)): #and not the same column #
                            return False
    return True

def init_board(file_name):
    """Creates a SudokuBoard object initialized with values from a text file"""
    board = parse_file(file_name)
    return SudokuBoard(len(board), board)


counter6 = 0

def solve(initial_board, forward_checking = False, MRV = False, MCV = False,
    LCV = False):
    """Takes an initial SudokuBoard and solves it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """
    global counter6
    if is_complete(initial_board) == True:
        print_board(initial_board)
        return initial_board
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    BoardChecker = initial_board.BoardChecker
    subsquare = int(math.sqrt(size))
    if MCV == True: #solve using most constrained variable (degree) heuristic
        for row in range(size):
            for col in range(size):
                if BoardArray[row][col]!=0: #if not empty space
                    update = BoardArray[row][col]
                    for i in range(size):
                        if i != col: #if not same
                            BoardChecker[row][i][update-1] = False #update row possibilities
                    for i in range(size):
                        if i != row: #if not same
                            BoardChecker[i][col][update-1] = False #update col possibilities
                    #determine which square the cell is in
                    SquareRow = row // subsquare
                    SquareCol = col // subsquare
                    for i in range(subsquare):
                        for j in range(subsquare):
                            if (SquareRow*subsquare+i != row) and (SquareCol*subsquare + j != col): #if not same
                                BoardChecker[SquareRow*subsquare+i][SquareCol*subsquare+j][update-1] = False #update subsquare possibilities
        #Finds empty cell that most affects other cells
        for row in range(size):
            for col in range(size):
                best = 0
                checker = 0
                print "At: ", row, " ", col
                if BoardArray[row][col]==0: #if empty space
                    for i in range(size):
                        if i != col:
                            if BoardArray[row][i]==0: #if empty space
                                checker = checker + 1
                    for i in range(size):
                        if i != row:
                            if BoardArray[i][col]==0: #if empty space
                                checker = checker + 1
                    #determine which square the cell is in
                    SquareRow = row // subsquare
                    SquareCol = col // subsquare
                    for i in range(subsquare):
                        for j in range(subsquare):
                            if (SquareRow*subsquare+i != row) and (SquareCol*subsquare + j != col): #if not same or column (already counted for)
                                if BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]==0: #if empty space
                                    checker = checker +1
                    print "Empty Spaces: ", checker
                    if checker > best or checker == 0: #checker still 0 if last empty cell on board
                        best = checker
                        bestRow = row
                        bestCol = col
        print "Best Checker: ", best
        for check in range(1, size+1):
            if BoardChecker[bestRow][bestCol][check-1]==True: #number could possibly work in the cell
                if conflictCheck(initial_board, bestRow, bestCol, check) == False: #no conflicts
                    for i in range(size):
                        if i != col: #if not same
                            BoardChecker[bestRow][i][check-1] = False #update row possibilities
                    for i in range(size):
                        if i != row: #if not same
                            BoardChecker[i][bestCol][check-1] = False #update col possibilities
                    #determine which square the cell is in
                    SquareRow = row // subsquare
                    SquareCol = col // subsquare
                    for i in range(subsquare):
                        for j in range(subsquare):
                            if (SquareRow*subsquare+i != bestRow) and (SquareCol*subsquare + j != bestCol): #if not same
                                BoardChecker[SquareRow*subsquare+i][SquareCol*subsquare+j][check-1] = False #update subsquare possibilities
                    new_initial_board = initial_board.set_value(bestRow,bestCol,check)
                    print_board(new_initial_board)
                    solve(new_initial_board, forward_checking, MRV, MCV, LCV) #recurse
                else:
                    BoardChecker[bestRow][bestCol][check-1]=False #number couldn't work in cell
                if is_complete(initial_board) != True:
                    initial_board = initial_board.set_value(bestRow,bestCol,0)
        return
    elif LCV == True: #solve using least constraining value heuristic
        for row in range(size):
            for col in range(size):
                if BoardArray[row][col]!=0: #if not empty space
                    update = BoardArray[row][col]
                    for i in range(size):
                        if i != col: #if not same
                            BoardChecker[row][i][update-1] = False #update row possibilities
                    for i in range(size):
                        if i != row: #if not same
                            BoardChecker[i][col][update-1] = False #update col possibilities
                    #determine which square the cell is in
                    SquareRow = row // subsquare
                    SquareCol = col // subsquare
                    for i in range(subsquare):
                        for j in range(subsquare):
                            if (SquareRow*subsquare+i != row) and (SquareCol*subsquare + j != col): #if not same
                                BoardChecker[SquareRow*subsquare+i][SquareCol*subsquare+j][update-1] = False #update subsquare possibilities
        for row in range(size):
            for col in range(size):
                if BoardArray[row][col]==0: #if empty space
                    bestFreq = size*size #value that least affects other cells
                    best = 0
                    listCheck = [[(size*size) for x in range(size)] for x in range(size)]
                    for check in range(1, size+1):
                        checker = 0
                        if BoardChecker[row][col][check-1]==True: #number could possibly work in the cell
                            for i in range(size):
                                if i != col:
                                    if BoardArray[row][i]==0: #if empty space
                                        if BoardChecker[row][i][check-1]==True: #check value also possible for other cell in col
                                            checker = checker +1
                            for i in range(size):
                                if i != row:
                                    if BoardArray[i][col]==0: #if empty space
                                        if BoardChecker[i][col][check-1]==True: #check value also possible for other cell in row
                                            checker = checker + 1
                            #determine which square the cell is in
                            SquareRow = row // subsquare
                            SquareCol = col // subsquare
                            for i in range(subsquare):
                                for j in range(subsquare):
                                    if (SquareRow*subsquare+i != row) and (SquareCol*subsquare + j != col): #if not same row or col
                                        if BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]==0: #if empty space
                                            if BoardChecker[SquareRow*subsquare+i][SquareCol*subsquare+j][check-1]==True:
                                                checker = checker + 1
                            if checker < bestFreq:
                                bestFreq = checker
                                best = check
                            if listCheck[0][0] == size*size: #list data is empty
                                listCheck[0][0] = check
                                listCheck[0][1] = checker
                            else:
                                n = 0
                                while listCheck[n][1]<checker: #while checker in list is < checker to add
                                    n = n+1 #find correct place in list to add new check to
                                for m in range (n+1, size-1): #move end of list over by 1 to make room for new check
                                    listCheck[m][0] = listCheck[m-1][0]
                                    listCheck[m][1] = listCheck[m-1][1]
                                listCheck[n][0] = check
                                listCheck[n][1] = checker
                    for best in range(0, size):
                        check = listCheck[best][0]
                        if check <= size:
                            if conflictCheck(initial_board, row, col, check) == False: #no conflicts
                                new_initial_board = initial_board.set_value(row,col,check) #fill space w number
                                new_initial_board.BoardChecker = initial_board.BoardChecker
                                for i in range(size):
                                    if i != col: #if not same
                                        BoardChecker[row][i][check-1] = False #update row possibilities
                                for i in range(size):
                                    if i != row: #if not same
                                        BoardChecker[i][col][check-1] = False #update col possibilities
                                #determine which square the cell is in
                                SquareRow = row // subsquare
                                SquareCol = col // subsquare
                                for i in range(subsquare):
                                    for j in range(subsquare):
                                        if (SquareRow*subsquare+i != row) and (SquareCol*subsquare + j != col): #if not same
                                            BoardChecker[SquareRow*subsquare+i][SquareCol*subsquare+j][check-1] = False #update subsquare possibilities
                                solve(new_initial_board, forward_checking, MRV, MCV, LCV) #recurse
                            else:
                                BoardChecker[row][col][best-1]=False #number couldn't work in cell
                            if is_complete(initial_board) != True:
                                initial_board = initial_board.set_value(row,col,0)
                    return
    elif MRV == True: #solve using min remaining values heuristic
        for row in range(size):
            for col in range(size):
                if BoardArray[row][col]!=0: #if not empty space
                    update = BoardArray[row][col]
                    for i in range(size):
                        if i != col: #if not same
                            BoardChecker[row][i][update-1] = False #update row possibilities
                    for i in range(size):
                        if i != row: #if not same
                            BoardChecker[i][col][update-1] = False #update col possibilities
                    #determine which square the cell is in
                    SquareRow = row // subsquare
                    SquareCol = col // subsquare
                    for i in range(subsquare):
                        for j in range(subsquare):
                            if (SquareRow*subsquare+i != row) and (SquareCol*subsquare + j != col): #if not same
                                BoardChecker[SquareRow*subsquare+i][SquareCol*subsquare+j][update-1] = False #update subsquare possibilities

        best = size
        for row in range(size):
            for col in range(size):
                if BoardArray[row][col]==0:
                    possibilities = 0
                    if possibilities < best:
                        best = possibilities
                        selectRow = row
                        selectCol = col
        for check in range(1,size+1):
            if BoardChecker[selectRow][selectCol][check-1]==True:
                if conflictCheck(initial_board, selectRow, selectCol, check) == False:
                    new_initial_board = initial_board.set_value(selectRow,selectCol,check)
                    for i in range(size):
                        if i != selectCol: #if not same
                            BoardChecker[selectRow][i][check-1] = False #update row possibilities
                    for i in range(size):
                        if i != selectRow: #if not same
                            BoardChecker[i][selectCol][check-1] = False #update col possibilities
                    #determine which square the cell is in
                    SquareRow = selectRow // subsquare
                    SquareCol = selectCol // subsquare
                    for i in range(subsquare):
                        for j in range(subsquare):
                            if (SquareRow*subsquare+i != selectRow) and (SquareCol*subsquare + j != selectCol): #if not same
                                BoardChecker[SquareRow*subsquare+i][SquareCol*subsquare+j][check-1] = False #update subsquare possibilities
                    solve(new_initial_board, forward_checking, MRV, MCV, LCV) #recurse
                else:
                    BoardChecker[selectRow][selectCol][check-1]=False #number couldn't work in cell
                if is_complete(initial_board) != True:
                    initial_board = initial_board.set_value(selectRow,selectCol,0)
        return
    elif forward_checking == True: #solve using forward checking
        for row in range(size):
            for col in range(size):
                if BoardArray[row][col]==0: #if empty space
                    for check in range(1, size+1):
                        if BoardChecker[row][col][check-1]==True: #number could possibly work in the cell
                            if conflictCheck(initial_board, row, col, check) == False: #no conflicts
                                new_initial_board = initial_board.set_value(row,col,check) #fill space w number
                                new_initial_board.BoardChecker = initial_board.BoardChecker
                                for i in range(size):
                                    if i != col: #if not same
                                        BoardChecker[row][i][check-1] = False #update row possibilities
                                for i in range(size):
                                    if i != row: #if not same
                                        BoardChecker[i][col][check-1] = False #update col possibilities
                                #determine which square the cell is in
                                SquareRow = row // subsquare
                                SquareCol = col // subsquare
                                for i in range(subsquare):
                                    for j in range(subsquare):
                                        if (SquareRow*subsquare+i != row) and (SquareCol*subsquare + j != col): #if not same
                                            BoardChecker[SquareRow*subsquare+i][SquareCol*subsquare+j][check-1] = False #update subsquare possibilities
                                solve(new_initial_board, forward_checking, MRV, MCV, LCV) #recurse
                            else:
                                BoardChecker[row][col][check-1]=False #number couldn't work in cell
                            if is_complete(initial_board) != True:
                                initial_board = initial_board.set_value(row,col,0)
                    return
    else: #solve using backtracking
        for row in range(size):
            for col in range(size):
                if BoardArray[row][col]==0: #if empty space
                    for check in range(1, size+1): #check all possible #'s in the space
                        if conflictCheck(initial_board, row, col, check) == False: #there's no conflicts
                            new_initial_board = initial_board.set_value(row,col,check)
                            solve(new_initial_board, forward_checking, MRV, MCV, LCV) #recurse
                            if is_complete(initial_board) != True:
                                initial_board = initial_board.set_value(row,col,0)
                    return

def conflictCheck(board, row, col, check):
    global counter6
    BoardArray = board.CurrentGameBoard
    size = len(BoardArray)
    counter6 = counter6 + 1
    subsquare = int(math.sqrt(size))
    if check == size + 2:
        return True
    for i in range(size):
        if ((BoardArray[row][i] == check) and i != col): #duplicate numbers in same row
            return True
        if ((BoardArray[i][col] == check) and i != row): #dupliacte numbers in same column
            return True
    #determine which square the cell is in
    SquareRow = row // subsquare
    SquareCol = col // subsquare
    for i in range(subsquare):
        for j in range(subsquare):
            if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                == check) #if there are any duplicates in the subsquare
                and (SquareRow*subsquare + i != row) #and not the same row #
                and (SquareCol*subsquare + j != col)): #and not the same column #
                return True
    return False



def print_board(self):
    """Prints the current game board. Leaves unassigned spots blank."""
    div = int(math.sqrt(self.BoardSize))
    dash = ""
    space = ""
    line = "+"
    sep = "|"
    for i in range(div):
        dash += "----"
        space += "    "
    for i in range(div):
        line += dash + "+"
        sep += space + "|"
        for i in range(-1, self.BoardSize):
            if i != -1:
                print "|",
                for j in range(self.BoardSize):
                    if self.CurrentGameBoard[i][j] > 9:
                        print self.CurrentGameBoard[i][j],
                    elif self.CurrentGameBoard[i][j] > 0:
                        print "", self.CurrentGameBoard[i][j],
                    else:
                        print "  ",
                    if (j+1 != self.BoardSize):
                        if ((j+1)//div != j/div):
                            print "|",
                        else:
                            print "",
                    else:
                        print "|"
            if ((i+1)//div != i/div):
                print line
            else:
                print sep

