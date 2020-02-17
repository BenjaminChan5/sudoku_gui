import pygame

class Cell:
    def __init__(self, num, row, col, width, height):
        self.num = num
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.tentative = 0 #tentative num for user input that hasn't been finalized
        self.selected = False #if this cell has been selected by the user

    def draw(self, window):
        font = pygame.font.SysFont("consolas", 40)

        size = int(self.width / 9)
        x_pos = self.col * size
        y_pos = self.row * size

        pygame.draw.rect(window, (0, 0, 0), (x_pos, y_pos, size, size), 1)

        if self.num != 0:
            text = font.render(str(self.num), 1, (0, 0, 0))
            window.blit(text, (x_pos + int(size / 2 - text.get_width() / 2), y_pos + int(size / 2 - text.get_height() / 2)))
        elif self.selected == True:
            pygame.draw.rect(window, (128, 128, 128), (x_pos, y_pos, size, size), 3)
            if self.tentative != 0:
                text = font.render(str(self.tentative), 1, (128, 128, 128))
                window.blit(text, (x_pos + int(size / 2 - text.get_width() / 2), y_pos + int(size / 2 - text.get_height() / 2)))

class Board:

    def __init__(self, window, rows, cols, width, height):
        self.window = window
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.values = [
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
        self.cells = []
        self.init_cells()
        self.text = None
        self.selected = None #selected is a tuple of integers to represent which cell is currently selected by the user

    def init_cells(self):
        for i in range(self.rows):
            self.cells.append([])
            for j in range(self.cols):
                self.cells[i].append(Cell(self.values[i][j], i, j, self.width, self.height))
                self.cells[i][j].draw(self.window)

    def select(self, row, col):
        if self.selected != None:
            self.cells[self.selected[0]][self.selected[1]].selected = False
        self.cells[row][col].selected = True
        self.selected = (row, col)

    def click(self, pos):
        # pos is the x and y position on screen
        # return the row and col of cell clicked (if applicable)
        # returns None if no cell clicked
        if pos[0] >= self.width or pos[1] >= self.height:
            return None

        size = int(self.width / 9)
        row = pos[1] // size
        col = pos[0] // size
        return (row, col)

    def tentative(self, num):
        self.cells[self.selected[0]][self.selected[1]].tentative = num

    def draw(self):
        self.window.fill((255,255,255))

        size = int(self.width / 9)
        for i in range(3, self.rows, 3):
            pygame.draw.line(self.window, (0, 0, 0), (0, i * size), (self.width, i * size), 5)
            pygame.draw.line(self.window, (0, 0, 0), (i * size, 0), (i * size, self.height), 5)

        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw(self.window)

        if self.solved():
            font = pygame.font.SysFont("consolas", 60)
            self.text = font.render("Congratulations!", 1, (0, 0, 0))
        if self.text != None:
            self.window.blit(self.text, (self.width//2 - self.text.get_width() // 2, self.height + 10))

    def reset_values(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.values[i][j] = self.cells[i][j].num

    def attempt(self, num):
        row, col = self.selected
        if self.cells[row][col].num == 0:
            self.values[row][col] = num
            if self.valid_move(num, self.selected) and self.solve():
                self.cells[row][col].num = num
                self.reset_values()
                return True
            else:
                self.cells[row][col].tentative = 0
                self.reset_values()
                return False
        return False

    def solve(self):
        # a board is represented as a 2D array
        # zeroes represent a box with no value
        # attempts to solve the board
        # returns True if board is solved
        # returns False if board is unsolvable
        pos = self.find_empty()
        if pos == None:
            return True
        for num in range(1, 10):
            # guess numbers and then check if it is a valid move
            # if move makes board unsolvable, returns and guesses a different number
            if self.valid_move(num, pos):
                self.values[pos[0]][pos[1]] = num
                if self.solve():
                    return True
                self.values[pos[0]][pos[1]] = 0  # reset the position back to 0
        return False  # if we get here then we tried all possible numbers and none worked

    def solve_update(self):
        font = pygame.font.SysFont("consolas", 60)
        self.text = font.render("Solving...", 1, (0, 0, 0))
        pos = self.find_empty()
        if pos == None:
            return True
        for num in range(1, 10):
            # guess numbers and then check if it is a valid move
            # if move makes board unsolvable, returns and guesses a different number
            if self.valid_move(num, pos):
                self.values[pos[0]][pos[1]] = num
                self.cells[pos[0]][pos[1]].num = num
                self.draw()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_update():
                    return True

                self.values[pos[0]][pos[1]] = 0  # reset the position back to 0
                self.cells[pos[0]][pos[1]].num = 0
                self.draw()
                pygame.display.update()
                pygame.time.delay(100)
        return False  # if we get here then we tried all possible numbers and none worked

    def solved(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j].num == 0:
                    return False
        return True

    def find_empty(self):
        # finds the first empty space
        # goes through first row then second etc.
        # returns (row, col) of empty space
        # returns None if there is no empty space
        for i in range(len(self.values)):
            for j in range(len(self.values[0])):
                if self.values[i][j] == 0:
                    return (i, j)
        return None

    def valid_move(self, num, pos):
        # board is a 2d array
        # num is the number that is being put at the position
        # pos is the position (row, col)
        # returns True if the move is valid, False if it isn't
        x = pos[0]
        y = pos[1]

        # check the row
        for j in range(len(self.values[0])):
            if self.values[x][j] == num and j != y:
                return False

        # check the column
        for i in range(len(self.values)):
            if self.values[i][y] == num and i != x:
                return False

        # check the box
        x = x - (x % 3)
        y = y - (y % 3)
        for i in range(x, x + 3):
            for j in range(y, y + 3):
                if self.values[i][j] == num and (pos[0], pos[1]) != (i, j):
                    return False

        return True


if __name__ == "__main__":
    pygame.init()
    width = 720
    height = 800
    screen = pygame.display.set_mode((width, height))

    pygame.display.set_caption("Sudoku")

    screen.fill((255, 255, 255))
    pygame.display.update()

    board = Board(screen, 9, 9, width, height - 80)
    pygame.display.update()

    print(pygame.font.get_fonts())

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9

                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None

                if event.key == pygame.K_SPACE:
                    board.solve_update()

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cells[i][j].tentative != 0:
                        font = pygame.font.SysFont("consolas", 60)
                        if board.attempt(board.cells[i][j].tentative):
                            print("Correct!")
                            board.text = font.render("Correct!", 1, (0, 0, 0))
                        else:
                            print("Wrong")
                            board.text = font.render("Wrong", 1, (0, 0, 0))
                        key = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected != None and key != None:
            board.tentative(key)

        board.draw()
        pygame.display.update()

    pygame.quit()
    exit()