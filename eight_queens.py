def printBoard(board):
    for i in range(len(board)):
        for j in range(len(board)):
            print(board[i][j],end=' ')
        print()
    
    # separator line is used to separate each solution/board
    separator = ''
    for i in range(len(board)):
        separator += '──'
        
    print(separator)

def countSolution(board, row):
    # global is used so that the counter is modified outside of the scope
    global counter
    
    # if all of the queens are placed on the board without threatening each other
    # which also means that the current row is equal to the size of the board
    # then print the board with all the queens
    # and increase the counter
    if row >= len(board):
        counter += 1
    
    for i in range(len(board)):
        
        # check if whether there are existing queens that will threaten the current queen
        # before placing a queen on the board
        if checkConstraints(board, row, i):
            
            # place queen on board[row][i]
            board[row][i] = 'Q'
 
            # recur for the next row on the board
            countSolution(board, row + 1)
 
            # backtrack and remove the queen to find the next solution
            board[row][i] = '·'

def placeQueen(board):
    row = 0
    column = 0
    while row in range(len(board)):
        while column in range(len(board)):
            if checkConstraints(board, row, column):
                board[row][column] = 'Q'
                row += 1
                column = 0
                break
            elif column + 1 == len(board):
                c = 0
                while c in range(len(board)):
                    if board[row-1][c] == 'Q':
                        board[row-1][c] = '·'
                        if row > 0:
                            row -= 1
                            column = c + 1
                        else:
                            row = 0
                            column = c + 1
                        if column < 4:
                            break
                        else:
                            c = 0
                            continue
                    else:
                        c += 1
            else:
                column += 1
                
        if row >= len(board):
            printBoard(board)
            
def checkColumn(chessBoard, row, column):
    # check if two queens are in the same column
    for r in range(row):
        if chessBoard[r][column] == 'Q':
            return False
    
    return True

def checkDiagonal(chessBoard, row, column):
    for r in range(len(chessBoard)):
        for c in range(len(chessBoard)):
            if (r + c == row + column) or (r - c == row - column):
                if chessBoard[r][c] == 'Q':
                    return False
    return True

def checkConstraints(chessBoard, row, column):
    
    # do not allow queens to be placed if the following constraints are met
    if checkColumn(chessBoard, row, column) and checkDiagonal(chessBoard, row, column):
        return True
    else:
        return False
    
if __name__ == '__main__':
 
    play = True
    
    print("Welcome to the nQueen world!")
    
    while play:
        valid = False

        while not valid: 
            try:
                N = int(input("Please enter the size of the board: "))
                valid = True
            except ValueError:
                print('Please only input digits') 
        
        print()
        
        # empty spot in the board is denoted by the symbol ·
        board = [['·' for x in range(N)] for y in range(N)]
        
        separator = ''
        for i in range(len(board)):
            separator += '──'
            
        print(separator)
        
        # counter is used to calculate the total number of solutions
        counter = 0
        
        # run the recursive function to find all solutions
        # placeQueen(board, 0)
        countSolution(board, 0)
        if N != 2 and N!= 3:
            placeQueen(board)
        
        # print the total number of solutions
        print("\nThere was a total of " + str(counter) + " solutions.")
        
        # to ask the user whether do they want to play another round
        again = str(input("Do you want to play again? (Y/N): "))
        if again.upper() == "N":
            play = False
