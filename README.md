
# Backgammon AI with Expectimax and Alpha-Beta Pruning

## 🎯 Introduction
This project is an AI-powered **Backgammon game** that uses the **Expectimax algorithm** combined with **Alpha-Beta Pruning** to make optimal decisions. The AI evaluates board states based on a heuristic function and simulates possible moves to determine the best strategy.

## 🚀 Features
- 🎲 **Dice Rolling Simulation** – Random dice rolls generate possible moves.
- ♟ **Board Representation** – Tracks the positions of pieces for both players.
- 🔄 **Move Execution & Undo** – Implements making and reversing moves for AI calculations.
- 🤖 **Expectimax AI** – AI searches the game tree for the best moves.
- ⚡ **Alpha-Beta Pruning** – Optimizes the search process by eliminating unnecessary branches.
- 📊 **Heuristic Evaluation** – Uses a scoring function to determine the best game states.

---

## 📦 Installation
Before running the game, install the required dependencies:

```sh
pip install tabulate
```
## ▶️ How to Run

Simply run the main script:
```sh
python main.py
```
The AI will play against itself, and the board state will be displayed after each move.

## 📂 Project Structure
```sh
📂 Backgammon-AI
│── 📄 Backgammon.py           # Abstract class defining the game structure
│── 📄 ExpectimaxBackgammon.py # AI implementation using Expectimax algorithm
│── 📄 main.py                 # Entry point to run the game
│── 📄 README.md               # Project documentation
```
## 🛠 How It Works

### 1️⃣ Board Representation

The board consists of 24 points, a bar, and bear-off areas. Pieces are stored in a list:
```sh
self.board: List[Tuple[int, Optional[str]]] = [[0, None] for _ in range(24)]
```
Each entry represents the number of pieces and the player ("white" or "black").

### 2️⃣ Rolling the Dice

The dice roll is simulated using:
```sh
def roll_dice(self) -> List[int]:
    return [random.randint(1, 6), random.randint(1, 6)]
```
This function generates two random numbers between 1 and 6.

### 3️⃣ Generating Possible Moves

The function get_possible_sequences() determines all valid moves based on the dice roll:
```sh
def get_possible_sequences(self, dice_roll: List[int]) -> List[List[Tuple[int, int]]]:
    # Generates all valid move sequences based on the dice values.
```
It accounts for blocked points, hitting opponent pieces, and bear-off conditions.

### 4️⃣ Move Execution & Undo

Each move modifies the game state:
```sh
def make_move(self, move: Tuple[int, int]) -> None:
    self.move_history.append((move, copy.deepcopy(self.board)))
    # Update board state based on move
```
To revert a move, the game restores the previous state:
```sh
def undo_move(self, move: Tuple[int, int]) -> None:
    self.board = self.move_history.pop()[1]
```
### 5️⃣ Expectimax Algorithm

The AI uses Expectimax, a variation of the Minimax algorithm that accounts for randomness in dice rolls:
```sh
def expectimax(self, depth: int, maximizing_player: bool, alpha, beta) -> float:
    if depth == 1 or self.is_game_over():
        return self.evaluate_board()

    dice_rolls = [(i, j) for i in range(1, 7) for j in range(1, 7)]
    if maximizing_player:
        max_eval = -float("inf")
        for dice_roll in dice_rolls:
            move_sequences = self.get_possible_sequences(list(dice_roll))
            for sequence in move_sequences:
                for move in sequence:
                    self.make_move(move)
                eval = self.expectimax(depth - 1, False, alpha, beta)
                for move in reversed(sequence):
                    self.undo_move(move)
                max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float("inf")
        for dice_roll in dice_rolls:
            move_sequences = self.get_possible_sequences(list(dice_roll))
            for sequence in move_sequences:
                for move in sequence:
                    self.make_move(move)
                eval = self.expectimax(depth - 1, True, alpha, beta)
                for move in reversed(sequence):
                    self.undo_move(move)
                min_eval = min(min_eval, eval)
        return min_eval

•	The AI recursively explores possible game states.
•	Maximizing player aims to maximize their advantage.
•	Minimizing player assumes the opponent will play optimally.
•	It evaluates board states using a heuristic function.
```
### 6️⃣ Heuristic Evaluation

The AI assigns a score to each board state:
```sh
def evaluate_board(self) -> int:
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

    return whiteScore - blackScore if not self.is_maximizing() else blackScore - whiteScore

•	Lower score → Better position for the AI.
•	Penalizes isolated pieces and pieces on the bar.
•	Rewards progress toward bear-off.
```
### 7️⃣ Alpha-Beta Pruning

To optimize Expectimax, Alpha-Beta Pruning reduces the number of states evaluated:
```sh
alpha = -float("inf")
beta = float("inf")

if beta <= alpha:
    break

•	Alpha tracks the best guaranteed value for the maximizer.
•	Beta tracks the best guaranteed value for the minimizer.
•	If Beta ≤ Alpha, further exploration is pruned.
```
### 8️⃣ Backgammon Board
🏆 Example Output
```sh
11 10  9  8  7  6  5  4  3  2  1  0
W5 -- -- -- B3 -- B5 -- -- -- -- W2
Bar: W-0 B-0
B5 -- -- -- W3 -- W5 -- -- -- -- B2
12 13 14 15 16 17 18 19 20 21 22 23
Bear Off: White - 0, Black - 0
```
### 9️⃣ Future Improvements

📌 Future Improvements
	•	📌 Train AI with Reinforcement Learning to improve decision-making.
	•	📌 Add a GUI for a visual representation of the board.
	•	📌 Support Multiplayer Mode to allow human vs AI gameplay.

👥 Contributors

👤 Mahsa Haghnevis – Developer
👤 Mahdi Mahmoudkhani – Developer
