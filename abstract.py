from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Optional

import random
random.seed(42)


class Backgammon(ABC):
    def __init__(self) -> None:
        self.board: List[Tuple[int, Optional[str]]] = [[0, None] for _ in range(24)]
        self.bar: Dict[str, int] = {"white": 0, "black": 0}
        self.bear_off: Dict[str, int] = {"white": 0, "black": 0}
        self.current_player: str = "white"
        self.initialize_board()
        self.move_history: List = []

    def initialize_board(self) -> None:
        self.board[0] = [2, "white"]
        self.board[11] = [5, "white"]
        self.board[16] = [3, "white"]
        self.board[18] = [5, "white"]
        self.board[23] = [2, "black"]
        self.board[12] = [5, "black"]
        self.board[7] = [3, "black"]
        self.board[5] = [5, "black"]

    @abstractmethod
    def get_possible_sequences(self, dice_roll: List[int]) -> List[List[Tuple[int, int]]]:
        pass

    def roll_dice(self) -> List[int]:
        return [random.randint(1, 6), random.randint(1, 6)]

    def change_player(self) -> None:
        self.current_player = "black" if self.current_player == "white" else "white"

    def is_maximizing(self) -> bool:
        return True if self.current_player == "white" else False

    @abstractmethod
    def make_move(self, move: Tuple[int, int]) -> None:
        pass

    @abstractmethod
    def undo_move(self, move: Tuple[int, int]) -> None:
        pass

    @abstractmethod
    def is_bear_off_possible(self) -> bool:
        pass

    def is_game_over(self) -> bool:
        return self.bear_off["white"] == 15 or self.bear_off["black"] == 15

    @abstractmethod
    def evaluate_board(self) -> int:
        pass

    def play_turn(self) -> None:
        dice_roll = self.roll_dice()
        print(f"{self.current_player} rolls: {dice_roll}")
        move_sequences = self.get_possible_sequences(dice_roll)

        if not move_sequences:
            print(f"{self.current_player} cannot move.")
            return

        best_sequence: Optional[List[Tuple[int, int]]] = None
        best_eval: float = -float("inf") if self.is_maximizing() else float("inf")

        alpha = -float("inf")
        beta = float("inf")

        for sequence in move_sequences:
            for move in sequence:
                self.make_move(move)
            self.change_player()
            
            eval = self.expectimax(self.max_depth, self.is_maximizing(), alpha, beta)

            self.change_player()
            for move in reversed(sequence):
                self.undo_move(move)
            if (self.is_maximizing() and eval > best_eval) or (
                not self.is_maximizing() and eval < best_eval
            ):
                best_eval = eval
                best_sequence = sequence

            if self.is_maximizing():
                alpha = max(alpha, eval)
            else:
                beta = min(beta, eval)

            if beta <= alpha:
                break

        if best_sequence:
            for move in best_sequence:
                self.make_move(move)
                print(f"{self.current_player} makes move: {move}")

    def play_game(self) -> None:
        while not self.is_game_over():
            self.display_board()
            self.play_turn()
            self.change_player()
        
        if self.is_game_over():
            winner = "white" if self.bear_off["white"] == 15 else "black"
            print(f"{winner} wins the game!")
            self.display_board()

    def display_board(self) -> None:
        print("\nBackgammon Board:")
        print(" ".join([f"{11 - i:2}" for i in range(12)]))
        print(" ".join([self.format_point(self.board[i]) for i in range(11, -1, -1)]))
        print(f"Bar: W-{self.bar['white']} B-{self.bar['black']}")
        print(" ".join([self.format_point(self.board[i]) for i in range(12, 24)]))
        print(" ".join([f"{i:2}" for i in range(12, 24)]))
        print(
            f"Bear Off: White - {self.bear_off['white']}, Black - {self.bear_off['black']}\n"
        )

    def format_point(self, point: Tuple[int, Optional[str]]) -> str:
        count, color = point
        if count == 0:
            return "--"
        return f"{color[0].upper()}{count}"