@@ -0,0 +1,83 @@
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Function to check if two queens threaten each other or not
def checkQueen(board, row, column):
 
    # return false if two queens share the same column
    for r in range(row):
        if board[r][column] == 'Q':
            return False
 
    # return false if two queens share the same `/` diagonal
    (i, j) = (row, column)
    while i >= 0 and j >= 0:
        if board[i][j] == 'Q':
            return False
        i -= 1
        j -= 1
 
    # return false if two queens share the same `/` diagonal
    (i, j) = (row, column)
    while i >= 0 and j < len(board):
        if board[i][j] == 'Q':
            return False
        i -= 1
        j += 1
 
    return True
 
 
def printSolution(board):
    for row in board:
        print(str(row).replace(',', '').replace('\'', ''))
    print()
 
def nQueen(board, row):
 
    # if `N` queens are placed successfully, print the solution
    if row >= len(board):
        printSolution(board)
 
    # place queen at every square in the current row `r`
    # and recur for each valid movement
    for i in range(len(board)):
 
        # if no two queens threaten each other
        if checkQueen(board, row, i):
            # place queen on the current square
            board[row][i] = 'Q'
 
            # recur for the next row
            nQueen(board, row + 1)
 
            # backtrack and remove the queen from the current square
            board[row][i] = ' '
            
    return True
 
if __name__ == '__main__':
 
    play = True
    
    while play:
        # `N × N` chessboard
        N = int(input("Please enter the size of the board: "))
        print()
     
        # `board[][]` keeps track of the position of queens in
        # the current configuration
        board = [[' ' for x in range(N)] for y in range(N)]
     
        if nQueen(board, 0) == True:
            print ("This is the end")
        else:
            print("No solution")
            
        again = str(input("Do you want to play again? (Y/N): "))
        if again.upper() == "N":
            play = False
            
        
    
 