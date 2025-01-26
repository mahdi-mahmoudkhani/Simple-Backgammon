from abstract import Backgammon

class MiniMaxBackgammon(Backgammon):
    
    def __init__(self) -> None:
        super().__init__()
        self.max_depth = 3

    def evaluate_board(self) -> int:
        '''
        This function uses an improved heuristic to evaluate the board.
        It calculates the distance of each piece to the bear off area, adds a penalty for pieces on the bar,
        rewards for pieces that have been borne off, and considers penalties for lonely pieces.
        It then sums the distances and calculates the difference between the sum of distances of white and black pieces.
        '''
        whiteScore = 0
        blackScore = 0
        for i in range(24):
            if self.board[i][1] == "white":
                whiteScore += (23 - i) * self.board[i][0]
                if self.board[i][0] == 1:  # Penalty for lonely pieces
                    whiteScore += 10
            elif self.board[i][1] == "black":
                blackScore += i * self.board[i][0]
                if self.board[i][0] == 1:  # Penalty for lonely pieces
                    blackScore += 10
        
        # Add penalties for pieces on the bar
        whiteScore += 24 * self.bar['white']
        blackScore += 24 * self.bar['black']
        
        # Add rewards for pieces that have been borne off
        whiteScore -= 15 * self.bear_off['white']
        blackScore -= 15 * self.bear_off['black']
        
        if self.current_player == "white":
            return whiteScore - blackScore
        return blackScore - whiteScore
        