import chess

class Status:
    Moved = 0
    Illegal = 1

class Board:
    board = chess.Board()

    def move(self, notation: str):
        move = chess.Move.from_uci(notation)

        if not move in self.board.legal_moves:
            return Status.Illegal

        self.board.push(move)

        return Status.Moved


    def string(self, white: bool, layout: tuple[int, int]):
        field_str = []

        field_str.append("g " * layout[0])

        if white:
            board_str = str(self.board)
        else:
            board_str = str(self.board)[::-1]

        for x, line in enumerate(board_str.splitlines()):
            field_str.append('g ' * ((layout[1] - 8) // 2))
            for y, character in enumerate(line.strip().split()):
                if (x + y) % 2 == 0:
                    field_str.append('T ')
                else:
                    field_str.append('t ')

                if character != '.':
                    field_str.append(f'{character} ')
            field_str.append('g ' * (((layout[1] - 8) // 2) + ((layout[1] - 8) % 2)))

        return ''.join(field_str)