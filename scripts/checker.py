import json

class GoWsChecker():
    """A Class to check correct words."""

    def __init__(self, s_game):

        self.letters = s_game.let
        
    def open_dictionary(self):
        """Open the dictionary from a json file."""
        filename = 'files/dictionary.json'

        with open(filename) as f:
            self.dictionary = json.load(f)
    
    def check_word(self, word_and_id):
        """Search for the word in a dictionary."""
        word = word_and_id[0]
        
        self.open_dictionary()

        if word.lower() in self.dictionary:
            awarded = [self.letters.letters[point][0] for point in word]

            self.points = sum(awarded)
            return self.points
        return None
