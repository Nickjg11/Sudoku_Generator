class Cell:
    """
    Cell class for storing a cell's info including the following:
    - the correct number that should be in the cell
    - the current guess for the number that should be in the cell
    - a boolean indicating whether the cell is a hint to be provided to the user
    """

    def __init__(self):
        """
        Create a Cell object with the correct, guess, and is_hint attributes
        """
        self.__correct = 0
        self.__guess = 0
        self.__is_hint = True

    def set_guess(self, num):
        """
        Set the Cell's guess attribute to the given number
        :param num: an integer in [1, 9]
        """
        self.__guess = num

    def get_guess(self):
        """
        Return the Cell's guess attribute
        :return: self.__guess -> an integer in [1, 9]
        """
        return self.__guess

    def set_correct(self, num):
        """
        Sets the Cell's correct attribute to the given num
        :param num: an integer in [1, 9]
        """
        self.__correct = num

    def get_correct(self):
        """
        Returns the Cell's correct attribute
        :return: self.__correct -> an integer in [1, 9]
        """
        return self.__correct

    def set_is_hint(self, b):
        """
        Sets the Cell's hint attribute to the given boolean
        :param b: a boolean
        """
        self.__is_hint = b

    def get_is_hint(self):
        """
        Returns True if the Cell's is_hint attribute is True, False otherwise
        :return: self.__is_hint -> boolean
        """
        return self.__is_hint
