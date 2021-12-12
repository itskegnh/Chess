from os import pipe


class Piece:
    def __init__(self, colour, char) -> None:
        self.colour = colour
        self.char = char
        self.has_moved = False

class Pawn(Piece):
    def __init__(self, colour) -> None:
        self.type, self.value = "Pawn", 100
        super().__init__(colour, "♙" if colour == 0 else "♟")

    def check_position(self, board, position, future_position) -> bool:
        if self.colour == 0: # white
            if position[1] - 1 == future_position[1] and position[0] == future_position[0]:
                return not board.get(future_position)
            if position[1] - 1 == future_position[1] and abs(position[0] - future_position[0]) == 1:
                if board.get(future_position) is None:
                    return False
                return not board.get(future_position).colour == self.colour
            if position[1] - 2 == future_position[1] and position[0] == future_position[0]:
                if position[1] != 6: return False
                return not board.get(future_position) and not board.get((position[0], position[1] - 1))
        if self.colour == 1: # black
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

    def calculate_moves(self, board, position) -> list:
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

class Knight(Piece):
    def __init__(self, colour, index=0) -> None:
        self.index = index
        self.type, self.value = "Knight", 300
        super().__init__(colour, "♘" if colour == 0 else "♞")
    
    def check_position(self, board, position, future_position) -> bool:
        if abs(position[0] - future_position[0]) == 2 and abs(position[1] - future_position[1]) == 1:
            if board.get(future_position) is None:
                return True
            return not board.get(future_position).colour == self.colour
        if abs(position[0] - future_position[0]) == 1 and abs(position[1] - future_position[1]) == 2:
            if board.get(future_position) is None:
                return True
            return not board.get(future_position).colour == self.colour

    def calculate_moves(self, board, position) -> list:
        legal_moves = []
        if self.check_position(board, position, (position[0] + 2, position[1] + 1)): legal_moves.append((position[0] + 2, position[1] + 1))
        if self.check_position(board, position, (position[0] + 2, position[1] - 1)): legal_moves.append((position[0] + 2, position[1] - 1))
        if self.check_position(board, position, (position[0] + 1, position[1] + 2)): legal_moves.append((position[0] + 1, position[1] + 2))
        if self.check_position(board, position, (position[0] + 1, position[1] - 2)): legal_moves.append((position[0] + 1, position[1] - 2))
        if self.check_position(board, position, (position[0] - 1, position[1] + 2)): legal_moves.append((position[0] - 1, position[1] + 2))
        if self.check_position(board, position, (position[0] - 1, position[1] - 2)): legal_moves.append((position[0] - 1, position[1] - 2))
        if self.check_position(board, position, (position[0] - 2, position[1] + 1)): legal_moves.append((position[0] - 2, position[1] + 1))
        if self.check_position(board, position, (position[0] - 2, position[1] - 1)): legal_moves.append((position[0] - 2, position[1] - 1))
        return legal_moves

class Rook(Piece):
    def __init__(self, colour) -> None:
        self.type, self.value = "Rook", 500
        super().__init__(colour, "♖" if colour == 0 else "♜")

    def calculate_moves(self, board, position) -> list:
        legal_moves = []
        for i in range(position[0] + 1, 8):
            if board.get((i, position[1])) is None:
                legal_moves.append((i, position[1]))
            elif board.get((i, position[1])) and board.get((i, position[1])).colour != self.colour:
                legal_moves.append((i, position[1]))
                break
            else:
                break
        for i in range(position[0] - 1, -1, -1):
            if board.get((i, position[1])) is None:
                legal_moves.append((i, position[1]))
            elif board.get((i, position[1])) and board.get((i, position[1])).colour != self.colour:
                legal_moves.append((i, position[1]))
                break
            else:
                break
        for i in range(position[1] + 1, 8):
            if board.get((position[0], i)) is None:
                legal_moves.append((position[0], i))
            elif board.get((position[0], i)) and board.get((position[0], i)).colour != self.colour:
                legal_moves.append((position[0], i))
                break
            else:
                break
        for i in range(position[1] - 1, -1, -1):
            if board.get((position[0], i)) is None:
                legal_moves.append((position[0], i))
            elif board.get((position[0], i)) and board.get((position[0], i)).colour != self.colour:
                legal_moves.append((position[0], i))
                break
            else:
                break
        return legal_moves

class Bishop(Piece):
    def __init__(self, colour) -> None:
        self.type, self.value = "Bishop", 330
        super().__init__(colour, "♗" if colour == 0 else "♝")

    def calculate_moves(self, board, position) -> list:
        legal_moves = []
        for i in range(1, 8):
            if board.get((position[0] + i, position[1] + i)) is None:
                legal_moves.append((position[0] + i, position[1] + i))
            elif board.get((position[0] + i, position[1] + i)) and board.get((position[0] + i, position[1] + i)).colour != self.colour:
                legal_moves.append((position[0] + i, position[1] + i))
                break
            else:
                break
        for i in range(1, 8):
            if board.get((position[0] + i, position[1] - i)) is None:
                legal_moves.append((position[0] + i, position[1] - i))
            elif board.get((position[0] + i, position[1] - i)) and board.get((position[0] + i, position[1] - i)).colour != self.colour:
                legal_moves.append((position[0] + i, position[1] - i))
                break
            else:
                break
        for i in range(1, 8):
            if board.get((position[0] - i, position[1] + i)) is None:
                legal_moves.append((position[0] - i, position[1] + i))
            elif board.get((position[0] - i, position[1] + i)) and board.get((position[0] - i, position[1] + i)).colour != self.colour:
                legal_moves.append((position[0] - i, position[1] + i))
                break
            else:
                break
        for i in range(1, 8):
            if board.get((position[0] - i, position[1] - i)) is None:
                legal_moves.append((position[0] - i, position[1] - i))
            elif board.get((position[0] - i, position[1] - i)) and board.get((position[0] - i, position[1] - i)).colour != self.colour:
                legal_moves.append((position[0] - i, position[1] - i))
                break
            else:
                break
        return legal_moves