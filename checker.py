import json

class ScrabbleChecker:
    """A Class to check correct words."""

    def __init__(self, s_game):

        self.letters = s_game.let

        self.open_dictionary()
        
    def open_dictionary(self):
        """Open the dictionary from a json file."""
        filename = 'files/scrabble_dic.json'

        with open(filename) as f:
            self.dictionary = json.load(f)
    
    def check_word(self, word):
        """Search for the word in a dictionary."""
        if word.lower() in self.dictionary:
            gathered = [self.letters.letters[point][0] for point in word]

            self.points = sum(gathered)
            return self.points
        return None