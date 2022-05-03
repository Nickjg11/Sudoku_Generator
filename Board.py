import numpy as np
import random
from Cell import Cell


class Board:
    """
    Board class for creating a solvable sudoku board and storing its info including:
    - a numpy array of Cells representing the cells in a Sudoku board
    """

    # starting board template used to set initial correct numbers of the board
    starting_board = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
                      [4, 5, 6, 7, 8, 9, 1, 2, 3],
                      [7, 8, 9, 1, 2, 3, 4, 5, 6],
                      [2, 3, 1, 5, 6, 4, 8, 9, 7],
                      [5, 6, 4, 8, 9, 7, 2, 3, 1],
                      [8, 9, 7, 2, 3, 1, 5, 6, 4],
                      [3, 1, 2, 6, 4, 5, 9, 7, 8],
                      [6, 4, 5, 9, 7, 8, 3, 1, 2],
                      [9, 7, 8, 3, 1, 2, 6, 4, 5]]

    def __init__(self, rand_seed):
        """
        Creates a Board object with the cells and num_solutions attributes
        :param rand_seed: seed with which to create the board - allows the same board to be generated
                                                                multiple times by identifying its seed
        """
        # sets the seed for random numbers to be generated the same way for the same seed
        random.seed(rand_seed)

        # create an empty numpy array which will hold Cell objects
        self.cells = np.empty([9, 9], dtype=Cell)

        # instantiate each Cell in the array and sets its correct number to the respective
        # value in the starting board template
        for i in range(0, 9):
            for j in range(0, 9):
                self.cells[i, j] = Cell()
                self.cells[i, j].set_correct(self.starting_board[i][j])

        # randomly shuffle the board so that the correct attributes no longer match up with
        # the template values
        self.__shuffle_all()

        # decide which cells should be hints given to the player
        self.__make_hints()

    def __swap_nums(self, num1, num2):
        """
        Swaps the correct placements of the first input number with the second input number and vice versa
        :param num1: an integer in [1, 9]
        :param num2: an integer in [1, 9]
        """
        for i in range(0, 9):
            for j in range(0, 9):
                # find a cell whose correct number is one of the inputs and change
                # it to the other input
                if self.cells[i][j].get_correct() == num1:
                    self.cells[i][j].set_correct(num2)
                elif self.cells[i][j].get_correct() == num2:
                    self.cells[i][j].set_correct(num1)

    def __shuffle_nums(self):
        """
        Swaps the correct placements of each number in [1, 9] with a random number in [1, 9]
        """
        for i in range(1, 10):
            self.__swap_nums(i, random.randrange(1, 10))

    def __swap_columns(self, c1, c2):
        """
        Swaps the placement of the first column with the second column and vice versa
        :param c1: an integer in [0, 8]
        :param c2: an integer in [0, 8]
        """
        temp = np.array(self.cells[:, c1])
        self.cells[:, c1] = self.cells[:, c2]
        self.cells[:, c2] = temp

    def __shuffle_columns(self):
        """
        Swaps each column with a random column
        """
        for i in range(0, 9):
            self.__swap_columns(i, (i // 3) * 3 + random.randrange(0, 3))

    def __swap_vertical_blocks(self, vb1, vb2):
        """
        Swaps the first input vertical block with the second input vertical block
        and vice versa
        Note: A vertical block is as follows:
                0 - columns 0, 1, 2
                1 - columns 3, 4, 5
                2 - columns 6, 7, 8
        :param vb1: an integer in [0, 2]
        :param vb2: an integer in [0, 2]
        """
        for i in range(0, 3):
            self.__swap_columns(vb1 * 3 + i, vb2 * 3 + i)

    def __shuffle_vertical_blocks(self):
        """
        Swaps each vertical block with a random vertical block
        Note: A vertical block is as follows:
                0 - columns 0, 1, 2
                1 - columns 3, 4, 5
                2 - columns 6, 7, 8
        """
        for i in range(0, 3):
            self.__swap_vertical_blocks(i, random.randrange(0, 3))

    def __swap_rows(self, r1, r2):
        """
        Swaps the placement of the first row with the second row and vice versa
        :param r1: an integer in [0, 8]
        :param r2: an integer in [0, 8]
        """
        temp = np.array(self.cells[r1, :])
        self.cells[r1, :] = self.cells[r2, :]
        self.cells[r2, :] = temp

    def __shuffle_rows(self):
        """
        Swaps each row with a random row
        """
        for i in range(0, 9):
            self.__swap_rows(i, (i // 3) * 3 + random.randrange(0, 3))

    def __swap_horizontal_blocks(self, hb1, hb2):
        """
        Swaps the first input horizontal block with the second input horizontal block
        and vice versa
        Note: A horizontal block is as follows:
                0 - rows 0, 1, 2
                1 - rows 3, 4, 5
                2 - rows 6, 7, 8
        :param hb1: an integer in [0, 2]
        :param hb2: an integer in [0, 2]
        """
        for i in range(0, 3):
            self.__swap_rows(hb1 * 3 + i, hb2 * 3 + i)

    def __shuffle_horizontal_blocks(self):
        """
        Swaps each horizontal block with a random horizontal block
        Note: A horizontal block is as follows:
                0 - rows 0, 1, 2
                1 - rows 3, 4, 5
                2 - rows 6, 7, 8
        """
        for i in range(0, 3):
            self.__swap_horizontal_blocks(i, random.randrange(0, 3))

    def __shuffle_all(self):
        """
        Shuffles all the columns, rows, vertical blocks, horizontal blocks, and numbers
        """
        self.__shuffle_vertical_blocks()
        self.__shuffle_horizontal_blocks()
        self.__shuffle_columns()
        self.__shuffle_rows()
        self.__shuffle_nums()

    def __check_row_allowed(self, r, c, num):
        """
        Checks the rest of the given row (r) to see if the given number (num)
        is a valid guess for the cell in the given row (r) and the given column (c)
        :param r: an integer in [0, 8]
        :param c: an integer in [0, 8]
        :param num: an integer in [1, 9]
        :return: True if the row does not have a hint or a guess that is the given number,
                 False otherwise
        """

        # check each cell in the row
        for col in range(0, 9):

            # ignore the cell that we are checking is valid
            if col != c:

                # check if there is a hint that is the same as the number
                if self.cells[r][col].get_is_hint():
                    if self.cells[r][col].get_correct() == num:
                        return False
                    else:
                        continue

                # check if there is another cell that has already guessed the number
                else:
                    if self.cells[r][col].get_guess() == num:
                        return False
                    else:
                        continue
        return True

    def __check_col_allowed(self, r, c, num):
        """
        Checks the rest of the given column (c) to see if the given number (num)
        is a valid guess for the cell in the given row (r) and the given column (c)
        :param r: an integer in [0, 8]
        :param c: an integer in [0, 8]
        :param num: an integer in [1, 9]
        :return: True if the column does not have a hint or a guess that is the given number,
                 False otherwise
        """

        # check each cell in the column
        for row in range(0, 9):

            # ignore the cell that we are checking is valid
            if row != r:

                # check if there is a hint that is the same as the number
                if self.cells[row][c].get_is_hint():
                    if self.cells[row][c].get_correct() == num:
                        return False
                    else:
                        continue

                # check if there is another cell that has already guessed the number
                else:
                    if self.cells[row][c].get_guess() == num:
                        return False
                    else:
                        continue
        return True

    def __check_block_allowed(self, r, c, num):
        """
        Checks the rest of the block containing the cell in the given row (r) and given column (c)
        to see if the given number (num) is a valid guess for the cell in the given row (r) and
        the given column (c)
        :param r: an integer in [0, 8]
        :param c: an integer in [0, 8]
        :param num: an integer in [1, 9]
        :return: True if the block does not have a hint or a guess that is the given number,
                 False otherwise
        """

        # divide the board into 3x3 blocks each with 3x3 cells
        block_r = r // 3
        block_c = c // 3
        for row in range(0, 3):
            for col in range(0, 3):

                # ignore the cell that we are checking is valid
                if col != c % 3 and row != r % 3:
                    # check if there is a hint that is the same as the number
                    if self.cells[row + block_r * 3][col + block_c * 3].get_is_hint():
                        if self.cells[row + block_r * 3][col + block_c * 3].get_correct() == num:
                            return False
                        else:
                            continue

                    # check if there is another cell that has already guessed the number
                    else:
                        if self.cells[row + block_r * 3][col + block_c * 3].get_guess() == num:
                            return False
                        else:
                            continue
        return True

    def __backtrack(self):
        """
        Solves the board based off of only the hints the board currently has.
            Works by guessing a number in the first cell and checking if it is allowed
            If it is, it moves on to the next cell and repeats this process
            If it is not, it guesses the next number
                If the next number is > 9 it goes back a cell guesses the next number for that cell
        Note: Requires that the board have at least one solution
        :return: the integer 1 if the board has only one possible solution or the integer 2
                 if the board has multiple possible solutions
        """

        # r and c control which row and column are being guessed
        r = 0
        c = 0

        # indicates whether we are moving forward to make a new guess or
        # moving backwards to change an old guess,
        dir = 1
        num_solutions = 0

        # controls when the board will stop finding solutions
        done_backtracking = False

        while not done_backtracking:

            # coming to the first cell with a 9 as the guess or a hint in the
            # first cell while moving backwards means we have no more possible solutions
            if r == 0 and c == 0 and (self.cells[r][c].get_guess() == 9 or \
                                      (dir == -1 and self.cells[r][c].get_is_hint())):
                done_backtracking = True

            # cell is a hint
            elif self.cells[r][c].get_is_hint():

                # trying to move forward to make a new guess
                if dir == 1:
                    # if we are on the last cell and trying to make a new guess, that means all
                    # of our guesses are valid, so we have found a solution
                    if r == 8 and c == 8:
                        num_solutions += 1

                        # only need to know if there is a single solution vs multiple so
                        # return the number of solutions when we reach 2
                        if num_solutions == 2:
                            done_backtracking = True

                        # go back and continue finding another solution
                        c -= 1
                        dir = -1

                    # skip to the next cell to make the new guess
                    elif c == 8:
                        r += 1
                        c = 0
                    else:
                        c += 1

                # trying to move backward to change previous guess
                else:
                    # skip to the previous cell to change the previous guess
                    if c == 0:
                        r -= 1
                        c = 8
                    else:
                        c -= 1

            # cell is not a hint
            else:

                # guess the next number
                self.cells[r][c].set_guess(self.cells[r][c].get_guess() + 1)

                # the guess is allowed
                if self.cells[r][c].get_guess() <= 9 and \
                        self.__check_row_allowed(r, c, self.cells[r][c].get_guess()) and \
                        self.__check_col_allowed(r, c, self.cells[r][c].get_guess()) and \
                        self.__check_block_allowed(r, c, self.cells[r][c].get_guess()):

                    # if we are on the last cell and the guess is allowed, we have found a solution
                    if r == 8 and c == 8:
                        num_solutions += 1

                        # only need to know if there is a single solution vs multiple so
                        # return the number of solutions when we reach 2
                        if num_solutions == 2:
                            done_backtracking = True

                        # set the guess to zero, then go back and continue finding another solution
                        self.cells[r][c].set_guess(0)
                        c -= 1
                        dir = -1

                    # make a new guess in the next cell
                    elif c == 8:
                        r += 1
                        c = 0
                        dir = 1
                    else:
                        c += 1
                        dir = 1

                # the guess is not allowed
                else:

                    # we have already guessed all numbers 1-9
                    if self.cells[r][c].get_guess() > 9:

                        # set guess back to zero
                        self.cells[r][c].set_guess(0)

                        # go back and change previous guess
                        if c == 0:
                            r -= 1
                            c = 8
                            dir = -1
                        else:
                            c -= 1
                            dir = -1

                    # we have not guessed all numbers 1-9
                    else:

                        # guess the next number
                        dir = 1
                        continue

        # set all guesses back to zero
        for i in range(0, 9):
            for j in range(0, 9):
                self.cells[i][j].set_guess(0)

        return num_solutions

    def __make_hints(self):

        # board starts with all cells being hints so there is only one possible solution
        unique_solution = True

        # remove hints until multiple solutions then add back the last hint removed
        while unique_solution:

            # board has one solution with current hints
            if self.__backtrack() == 1:

                # choose a random hint to take away
                i = random.randrange(0, 9)
                j = random.randrange(0, 9)
                while not self.cells[i][j].get_is_hint():
                    i = random.randrange(0, 9)
                    j = random.randrange(0, 9)
                self.cells[i][j].set_is_hint(False)

            # board has more than one solution with current hints
            else:

                # stop removing hints
                unique_solution = False

                # restore the previous hint that was taken away
                self.cells[i][j].set_is_hint(True)

                # set all guesses to None, as no guesses by the user have been made
                for i in range(0, 9):
                    for j in range(0, 9):
                        self.cells[i][j].set_guess(None)

a = Board(12)