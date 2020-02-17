def solve(board):
    # a board is represented as a 2D array
    # zeroes represent a box with no value
    # attempts to solve the board
    # returns True if board is solved
    # returns False if board is unsolvable
    pos = find_empty(board)
    if pos == None:
        return True

    for num in range(1, 10):
        # guess numbers and then check if it is a valid move
        # if move makes board unsolvable, returns and guesses a different number
        if valid_move(board, num, pos):
            board[pos[0]][pos[1]] = num

            if solve(board):
                return True

            board[pos[0]][pos[1]] = 0 # reset the position back to 0

    return False # if we get here then we tried all possible numbers and none worked

def find_empty(board):
    # finds the first empty space
    # goes through first row then second etc.
    # returns (row, col) of empty space
    # returns None if there is no empty space
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)
    return None

def print_board(board):
    # a board is represented as a 2D array
    # prints out the board
    for i in range(len(board)):
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print("| ", end = "")
            num = board[i][j]
            if num == 0:
                print(" ", end = " ")
            else:
                print(num, end = " ")
        print()
        if i % 3 == 2 and i != 8:
            print("----------------------")

def valid_move(bo, num, pos):
    # board is a 2d array
    # num is the number that is being put at the position
    # pos is the position (row, col)
    # returns True if the move is valid, False if it isn't
    x = pos[0]
    y = pos[1]

    # check the row
    for j in range(len(board[0])):
        if board[x][j] == num and j != y:
            return False

    # check the column
    for i in range(len(board)):
        if board[i][y] == num and i != x:
            return False

    # check the box
    x = x - (x % 3)
    y = y - (y % 3)
    for i in range(x, x+3):
        for j in range(y, y+3):
            if board[i][j] == num and (x,y) != (i,j):
                return False

    return True


if __name__ == "__main__":
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]
    print_board(board)
    solve(board)
    print()
    print_board(board)