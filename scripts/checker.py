import json

class GoWsChecker():
    """A Class to check correct words."""

    def __init__(self, game):

        self.letters = game.let
        
    def open_dictionary(self):
        """Open the dictionary from a json file."""
        filename = 'files/dictionary.json'

        with open(filename) as f:
            self.dictionary = json.load(f)
    
    def check_word(self, word):
        """Search for the word in a dictionary."""

        self.open_dictionary()

        if word.lower() in self.dictionary:
            awarded = [self.letters.letters[let][0] for let in word]

            self.points = sum(awarded)
            return self.points
        return None
