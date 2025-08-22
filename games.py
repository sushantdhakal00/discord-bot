# games.py

class TicTacToe:
    def __init__(self, player1_id: int, player2_id: int):
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.board = [" "] * 9
        self.turn = player1_id  # Player1 starts
        self.winner = None
        self.game_over = False

    def make_move(self, player_id: int, position: int):
        if self.game_over:
            return False, "Game already over."
        if player_id != self.turn:
            return False, "It's not your turn."
        if not (0 <= position <= 8):
            return False, "Invalid position (0-8)."
        if self.board[position] != " ":
            return False, "Position already taken."

        mark = "X" if player_id == self.player1_id else "O"
        self.board[position] = mark

        # Check win/draw
        if self.check_winner(mark):
            self.winner = player_id
            self.game_over = True
            return True, f"{mark} wins!"
        elif " " not in self.board:
            self.winner = None
            self.game_over = True
            return True, "It's a draw."

        # Switch turn
        self.turn = self.player2_id if self.turn == self.player1_id else self.player1_id
        return True, None

    def check_winner(self, mark: str):
        wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        return any(self.board[a] == self.board[b] == self.board[c] == mark for a, b, c in wins)
