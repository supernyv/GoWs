class ScrabbleStats:
    """A Class to manage all the game stats."""
    def __init__(self, s_game):
        """Initialize game stats."""
        self.reset_stats()
        self.reset_news()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.player_1_score = 00
        self.player_2_score = 00
    
    def reset_news(self):
        self.news = ""