from Board import Board
from functools import partial
import tkinter as tk
import random


class Game:

    def __init__(self):
        """
        Creates graphical user interface that displays a representation of the current
        state of the sudoku board and buttons in order to change the state of the board
        """

        # instantiate necessary attributes
        self.__highlight_toggle = False
        self.__solution_toggle = False
        self.__selection = 0
        self.__board = Board(random.randrange(0, 1000000))
        self.__buttons = []
        self.__selectors = []

        # create and name the window
        window = tk.Tk()
        window.title("Sudoku")

        # menu frame to hold the selection area for the selection buttons, new game button,
        # random seed label, random seed entry, toggle highlight button, and toggle solution button
        menu = tk.Frame(
            master=window,
            height=500,
            width=250,
            bg="white",
            borderwidth=5
        )

        # create the new game button, random seed label, random
        # seed entry, toggle highlight button, and toggle solution button
        lbl_rand_seed = tk.Label(master=menu, text="Seed for board")
        self.__ent_rand_seed = tk.Entry(master=menu)
        btn_new_game = tk.Button(master=menu, text="New Game", command=lambda: self.__new_game(self.__ent_rand_seed.get()))
        btn_highlight = tk.Button(master=menu, text="Highlight Guesses", command=self.__toggle_highlight)
        btn_solution = tk.Button(master=menu, text="Toggle Solution", command=self.__toggle_solution)

        # position the new game button, random seed label, random
        # seed entry, toggle highlight button, and toggle solution button
        # above each other
        btn_new_game.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        lbl_rand_seed.grid(row=1, column=0, sticky="ew", padx=5)
        self.__ent_rand_seed.grid(row=2, column=0, sticky="ew", padx=5)
        btn_highlight.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        btn_solution.grid(row=4, column=0, sticky="ew", padx=5, pady=5)

        # create frame in the menu area to hold the selection buttons
        selection_area = tk.Frame(
            master=menu,
            width=100,
            height=100,
            bg="white"
        )

        # create selection buttons
        for i in range(0,3):
            for j in range(0, 3):
                frame = tk.Frame(
                    master=selection_area,
                    relief=tk.RAISED,
                    borderwidth=1
                )
                frame.grid(row=i, column=j)
                button = tk.Button(
                    master=frame,

                    # should be able to select numbers 1-9 to make a guess in the board
                    text=(i * 3 + 1) + j,
                    bg="light grey",
                    width=4,
                    height=2,

                    # change my current selection to the pressed button and highlight the new selection
                    command=partial(self.__update_selection, ((i * 3 + 1) + j))
                )

                # add new selection button to the list of selection buttons so that
                # each unique button can be referenced using the command since each button has
                # the same name
                self.__selectors += [button]
                button.pack(expand=True)

        # place selection board below other items in the menu area
        selection_area.grid(
            row=5,
            column=0,
            sticky="ew",
            padx=5,
            pady=5
        )
        menu.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # create frame to hold sudoku board buttons
        board_area = tk.Frame(
            master=window,
            width=500,
            height=500,
            bg="white"
        )

        # create board buttons
        for i in range(0, 9):
            for j in range(0, 9):
                frame = tk.Frame(
                    master=board_area,
                    relief=tk.RAISED,
                    borderwidth=1
                )
                frame.grid(row=i, column=j)
                button = tk.Button(
                    master=frame,

                    # when the board button is created it should display
                    # the correct number if the respective cell is a hint or blank
                    # since no guess has been made yet
                    text=self.__cell_to_text(i, j),
                    bg="white",
                    width=4,
                    height=2,

                    # should change guess to current selection when button is pressed
                    command=partial(self.__make_guess, i, j)
                )
                self.__buttons += [button]
                button.pack(expand=True)
        board_area.pack(side=tk.LEFT, expand=True)

        # highlight the hints in the board buttons so the user can tell
        # the difference between hints and their guesses
        self.__change_background_colors()

        window.mainloop()

    def __new_game(self, rand_seed):
        """
        Generates a different sudoku board using the given seed if it is a numeric string, and
        a random number otherwise
        :param rand_seed: a string
        """

        # seed is numeric string
        if rand_seed.isnumeric():

            # make new board with seed
            self.__board = Board(int(rand_seed))

        # seed is not numeric string
        else:

            # make new board with random number
            self.__board = Board(random.randrange(0, 1000000))

        # clear entry
        self.__ent_rand_seed.delete(0, 'end')

        # update buttons to reflect new board
        self.__update_buttons()

    def __update_buttons(self):
        """
        Updates the text and background color of the all the board buttons to display correctly
        """

        # update the text of the board buttons
        for b in range(0, 81):
            i = b // 9
            j = b % 9
            self.__buttons[b]['text'] = self.__cell_to_text(i, j)

        # update the colors of the board buttons
        self.__change_background_colors()

    def __toggle_highlight(self):
        """
        Toggles the highlight_toggle attribute and updates the background colors
        of the board buttons
        """

        # toggle the highlight
        self.__highlight_toggle = not self.__highlight_toggle

        # update the colors of the board buttons
        self.__change_background_colors()

    def __toggle_solution(self):
        """
        Toggles the solution_toggle attribute and updates the text and background colors
        of the board buttons
        """

        # toggle the solution
        self.__solution_toggle = not self.__solution_toggle

        # update the text and background colors of the board buttons
        self.__update_buttons()

    def __update_selection(self, num):
        """
        Updates the selection attribute to be the given number and updates the
        background colors of the previously chosen selection button and
        the newly chosen selection button
        :param num: an integer in [1, 9]
        """

        # update background color of previously chosen selection button
        self.__selectors[self.__selection - 1]['bg'] = "light grey"

        # update selection
        self.__selection = num

        # update background color of newly chosen selection button
        self.__selectors[num - 1]['bg'] = "light blue"

    def __change_background_colors(self):
        """
        Updates the background colors of all the board buttons
        """
        for i in range(0, 9):
            for j in range(0, 9):
                self.__change_background_color(i, j)

    def __change_background_color(self, i, j):
        """
        Change background color of the board button in the given row (i) and the
        given column (j)
        :param i: an integer in [0, 8]
        :param j: an integer in [0. 8]
        """

        # index of board button (corresponding to button in row i and column j) in list of buttons
        btn_index = i * 9 + j

        # displaying solutions as green
        if self.__solution_toggle:
            self.__buttons[btn_index]['bg'] = "green"

        # displaying incorrect guesses as red with correct guesses and hints as green
        elif self.__highlight_toggle:
            if self.__board.cells[i][j].get_is_hint() or \
                    self.__board.cells[i][j].get_guess() == self.__board.cells[i][j].get_correct():
                self.__buttons[btn_index]['bg'] = "green"
            else:
                self.__buttons[btn_index]['bg'] = "red"

        # displaying guesses as white and hints as light blue
        else:
            if self.__board.cells[i][j].get_is_hint():
                self.__buttons[btn_index]['bg'] = "light blue"
            else:
                self.__buttons[btn_index]['bg'] = "white"

    def __cell_to_text(self, i, j):

        # solution is toggled on so display correct
        if self.__solution_toggle:
            return self.__board.cells[i][j].get_correct()

        # cell is hint so display correct
        elif self.__board.cells[i][j].get_is_hint():
            return self.__board.cells[i][j].get_correct()

        # cell is guess so display guess
        else:
            if self.__board.cells[i][j].get_guess() is None:
                return ""
            else:
                return self.__board.cells[i][j].get_guess()

    def __make_guess(self, i, j):
        """
        Sets the guess of the cell in the given row (i) and given column (j)
        and the text of the board button in the given row (i) and given column (j)
        to the current selection
        :param i: an integer in [0, 8]
        :param j: an integer in [0, 8]
        """

        # cell not a hint and I have chosen a selection number
        if not self.__board.cells[i][j].get_is_hint() and not self.__selection == 0:
            self.__board.cells[i][j].set_guess(self.__selection)

        # index of board button (corresponding to button in row i and column j) in list of buttons
        btn_index = i * 9 + j

        # update the text of the board button in row i and column j
        self.__buttons[btn_index]['text'] = self.__cell_to_text(i, j)

        # update the background color of the board button in row i and column j
        self.__change_background_color(i, j)