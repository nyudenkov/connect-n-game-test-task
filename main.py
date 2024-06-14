import os

import click
import numpy as np


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


class ConnectNGame:
    def __init__(self, rows: int, cols: int, connect: int, players_num: int):
        # TODO: add check that field can be played for connect/players_num
        self.rows = rows
        self.cols = cols
        self.connect = connect
        self.board = np.zeros((rows, cols), dtype=int)
        self.players_num = players_num
        self.current_player = 1

    def print_board(self) -> None:
        print(f'Connect-{self.connect} Game')
        print(np.flip(self.board, 0))

    def drop_piece(self, col: int) -> bool:
        if self.board[self.rows - 1][col] != 0:
            return False

        for row in range(self.rows):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                break

        return True

    def check_winner(self) -> bool:
        # Checking horizontal line
        for row in range(self.rows):
            for col in range(self.cols - self.connect + 1):
                if np.all(self.board[row, col:col + self.connect] == self.current_player):
                    return True

        # Checking vertical line
        for row in range(self.rows - self.connect + 1):
            for col in range(self.cols):
                if np.all(self.board[row:row + self.connect, col] == self.current_player):
                    return True

        # Checking diagonal-right
        for row in range(self.rows - self.connect + 1):
            for col in range(self.cols - self.connect + 1):
                if np.all([self.board[row + i, col + i] == self.current_player for i in range(self.connect)]):
                    return True

        # Checking dialonal-left
        for row in range(self.rows - self.connect + 1):
            for col in range(self.cols - self.connect + 1):
                if np.all(
                        [
                            self.board[row + i, col + self.connect - 1 - i] == self.current_player
                            for i in range(self.connect)
                        ]
                ):
                    return True

        return False

    def switch_player(self) -> None:
        self.current_player = (self.current_player % self.players_num) + 1

    def is_draw(self) -> bool:
        return np.all(self.board != 0)

    def play(self):
        while True:
            cls()
            self.print_board()

            try:
                col = int(input(f"Player {self.current_player}, choose column (1-{self.cols}): ")) - 1
            except ValueError:
                continue

            if col < 0 or col >= self.cols or not self.drop_piece(col):
                continue

            if self.check_winner():
                cls()
                self.print_board()
                print(f"Player {self.current_player} wins!")
                break

            if self.is_draw():
                cls()
                self.print_board()
                print("Draw!")
                break

            self.switch_player()


@click.command('Game')
@click.option("--rows", type=int, default=6, help='Num of rows')
@click.option("--cols", type=int, default=7, help='Num of cols')
@click.option("--connect", type=int, default=4, help='Num of connected pieces')
@click.option("--players-num", type=int, default=2, help='Num of players')
def main(rows: int, cols: int, connect: int, players_num: int) -> None:
    print(rows, cols, connect, players_num)
    game = ConnectNGame(rows, cols, connect, players_num)
    game.play()


if __name__ == '__main__':
    main()
