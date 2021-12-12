class Piece:
    def __init__(self, colour, char) -> None:
        self.colour = colour
        self.char = char

class Pawn(Piece):
    def __init__(self, colour) -> None:
        super().__init__(colour, "♙" if colour == 0 else "♟")

    def check_position(self, board, position, future_position):
        if self.colour == 0: # white
            if position[1] - 1 == future_position[1] and position[0] == future_position[0]:
                return not board.get(future_position)
            if position[1] - 1 == future_position[1] and abs(position[0] - future_position[0]) == 1:
                if board.get(future_position) is None:
                    return False
                return not board.get(future_position).colour == self.colour
            if position[1] - 2 == future_position[1] and position[0] == future_position[0]:
                if position[1] != 6: return False
                return not board.get(future_position) and not board.get((position[0], position[1] + 1))
        if self.colour == 1: # black
            print(position[1], future_position[1])
            if position[1] + 1 == future_position[1] and position[0] == future_position[0]:
                
                return not board.get(future_position)
            if position[1] + 1 == future_position[1] and abs(position[0] - future_position[0]) == 1:
                if board.get(future_position) is None:
                    return False
                return not board.get(future_position).colour == self.colour
            if position[1] + 2 == future_position[1] and position[0] == future_position[0]:
                if position[1] != 1: return False
                return not board.get(future_position) and not board.get((position[0], position[1] + 1))
        return True
        
        # if position[1] == future_position[1] + 1 and position[0] == future_position[0]:
        #     return not board.get(future_position)
        # elif position[1] == future_position[1] + 1 and abs(position[0] - future_position[0]) == 1:
        #     return not board.get(future_position).colour == self.colour
        # elif position[1] == future_position[1] + 2 and position[0] == future_position[0] and position[1] == 1:
        #     return not (board.get(future_position) and board.get((position[0], position[1] + 1)))
        return True

    def calculate_moves(self, board, position):
        legal_moves = []
        if self.colour == 0: # white
            if self.check_position(board, position, (position[0], position[1] - 1)): legal_moves.append((position[0], position[1] - 1))
            if self.check_position(board, position, (position[0], position[1] - 2)): legal_moves.append((position[0], position[1] - 2))
            if self.check_position(board, position, (position[0] + 1, position[1] - 1)): legal_moves.append((position[0] + 1, position[1] - 1))
            if self.check_position(board, position, (position[0] - 1, position[1] - 1)): legal_moves.append((position[0] - 1, position[1] - 1))
        elif self.colour == 1: # black
            if self.check_position(board, position, (position[0], position[1] + 1)): legal_moves.append((position[0], position[1] + 1))
            if self.check_position(board, position, (position[0], position[1] + 2)): legal_moves.append((position[0], position[1] + 2))
            if self.check_position(board, position, (position[0] + 1, position[1] + 1)): legal_moves.append((position[0] + 1, position[1] + 1))
            if self.check_position(board, position, (position[0] - 1, position[1] + 1)): legal_moves.append((position[0] - 1, position[1] + 1))

        
        return legal_moves