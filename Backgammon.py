from abstract import Backgammon
from typing import List, Tuple, Dict, Optional
import copy


class MiniMaxBackgammon(Backgammon):
    
    def __init__(self) -> None:
        super().__init__()
        self.max_depth = 2

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
        
    def other_player(self, player: str) -> str:
        return "black" if player == "white" else "white"
        
    def make_move(self, move: Tuple[int, int]) -> None:
        self.move_history.append((move, copy.deepcopy(self.board), copy.deepcopy(self.bar), copy.deepcopy(self.bear_off)))

        start, end = move
        if start == 24 or start == -1:
            self.bar[self.current_player] -= 1
        elif self.board[start][0] == 1:
            self.board[start] = [0, None]
        else:
            self.board[start][0] -= 1

        if end == 24 or end == -1:
            self.bear_off[self.current_player] += 1
        else:
            if self.board[end][1] != self.current_player and self.board[end][0] == 1:
                self.board[end] = [1, self.current_player]
                self.bar[self.other_player(self.current_player)] += 1
            else:
                self.board[end] = [self.board[end][0] + 1, self.current_player]

    def undo_move(self, move: Tuple[int, int]) -> None:
        # use move history to undo the given move
        # first finidng the move in the move history
        for i in range(len(self.move_history) - 1, -1, -1):
            if self.move_history[i][0] == move:
                break
        self.board = self.move_history[i][1]
        self.bar = self.move_history[i][2]
        self.bear_off = self.move_history[i][3]
        self.move_history = self.move_history[:i]
    
    def is_bear_off_possible(self) -> bool:
        checkRange = range(18) if self.current_player == "white" else range(6, 24)
        for i in checkRange:
            if self.board[i][1] == self.current_player:
                return False
        return True
    
    def get_possible_sequences(self, dice_roll: List[int]) -> List[List[Tuple[int, int]]]:
        '''
        The idea is to generate all possible moves for each die in the dice roll and then combine them to form sequences.
        First we generate all possible moves for the first die, then for the second die.
        For each die, we start from the points where the current player has pieces and move them forward or backward based on the die value. Then we check if the end point is valid; If so we add the move to the list of possible moves.
        We then combine the moves for the two dice to form sequences.
        If the dice values are different, we also generate sequences for the reverse order of the dice values.
        '''

        def generate_moves(dice: List[int], player: str) -> List[List[Tuple[int, int]]]:
            '''
            Generate all possible moves for the given dice values. It does this by iterating over all points where the player has pieces and then moving them forward or backward based on the die value. Then add to the list of possible moves if the end point is valid.
            '''
            moves = []
            for die in dice:
                if self.bar[player] > 0:
                    # if player has pieces on the bar, only allow moves from the bar
                    if player == "white":
                        if self.board[die - 1][1] in [None, "white"]:
                            moves.append([(-1, die - 1)])
                    else:
                        if self.board[24 - die][1] in [None, "black"]:
                            moves.append([(24, 24 - die)])
                else:
                    for i in range(24):
                        if self.board[i][1] == player:
                            end_pos = i + die if player == "white" else i - die
                            if 0 <= end_pos < 24 and (self.board[end_pos][1] in [None, player] or self.board[end_pos][0] == 1):
                                moves.append([(i, end_pos)])
                            # if bearin off is possible, add bear off move
                            if self.is_bear_off_possible() and end_pos == 24 and player == "white":
                                moves.append([(i, 24)])
                            if self.is_bear_off_possible() and end_pos == -1 and player == "black":
                                moves.append([(i, -1)])
            return moves
        
        def generate_sequences(dice: List[int], player: str) -> List[List[Tuple[int, int]]]:
            '''
            Generate all possible sequences of moves for the given dice values. It does this by generating moves for the first die, applying each move, and then generating moves for the second die using the new board state.
            It handles both sequences: first dice 1 then dice 2 and first dice 2 then dice 1.
            '''
            sequences = []
            for order in [(0, 1), (1, 0)]:
                first_moves = generate_moves([dice[order[0]]], player)
                for first_move in first_moves:
                    self.make_move(first_move[0])
                    second_moves = generate_moves([dice[order[1]]], player)
                    if second_moves:
                        for second_move in second_moves:
                            sequences.append(first_move + second_move)
                    else: 
                        sequences.append(first_move + [])
                    self.undo_move(first_move[0])
            return sequences
        
        sequences = generate_sequences(dice_roll, self.current_player)

        # remove duplicates and sort the moves
        sequences = list(set([tuple(sorted(seq, reverse= self.current_player != "white")) for seq in sequences]))
        return sequences