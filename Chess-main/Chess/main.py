from typing import Text
import pygame
from pieces import *

pygame.font.init()

class Game:
    def __init__(self, size) -> None:
        self.colours = {
            "black": (118,150,86),
            "white": (238,238,210),
        }

        self.width, self.height = size, size
        self.cell_size = (self.width // 8, self.height // 8)
        self.axis_margin = size * 0.05

        self.screen = pygame.display.set_mode((self.width+self.axis_margin, self.height+self.axis_margin))
        self.screen.fill((255, 255, 255))

        self.selected = None

        self.board = {
            (0,0): Rook(1),
            (1,0): Knight(1,1),
            (2,0): Bishop(1),
            # (3,0): Queen(0),
            # (4,0): King(0),
            (5,0): Bishop(1),
            (6,0): Knight(1),
            (7,0): Rook(1),
            (0,1): Pawn(1),
            (1,1): Pawn(1),
            (2,1): Pawn(1),
            (3,1): Pawn(1),
            (4,1): Pawn(1),
            (5,1): Pawn(1),
            (6,1): Pawn(1),
            (7,1): Pawn(1),

            (0,6): Pawn(0),
            (1,6): Pawn(0),
            (2,6): Pawn(0),
            (3,6): Pawn(0),
            (4,6): Pawn(0),
            (5,6): Pawn(0),
            (6,6): Pawn(0),
            (7,6): Pawn(0),
            (7,7): Rook(0),
            (6,7): Knight(0),
            (5,7): Bishop(0),
            # (4,7): Queen(0),
            # (3,7): King(0),
            (2,7): Bishop(0),
            (1,7): Knight(0,1),
            (0,7): Rook(0),
        }

        self.last_move = None
        self.turn = 0

    def draw_board(self):
        self.screen.fill(self.colours["black"])
        pygame.draw.line(self.screen, (0,0,0), (self.axis_margin-1,0), (self.axis_margin-1,self.height), 1)
        pygame.draw.line(self.screen, (0,0,0), (self.axis_margin,self.height), (self.width+self.axis_margin,self.height), 1)
        pygame.draw.line(self.screen, (0,0,0), (self.width+self.axis_margin,0), (self.width+self.axis_margin,self.height), 1)
        label_font = pygame.font.SysFont("Arial", int(min(self.axis_margin, self.axis_margin)))
        piece_font = pygame.font.Font("FreeSerif.otf", int(self.cell_size[0]*0.75))
        for i in range(8):
            x = label_font.render(str(chr(i+65)), True, self.colours["white"])
            y = label_font.render(str(8-i), True, self.colours["white"])
            self.screen.blit(x, (self.axis_margin+i*self.cell_size[0]+self.cell_size[0]//2-x.get_width()//2, self.height+(self.axis_margin//2)-x.get_height()//2))
            self.screen.blit(y, (self.axis_margin//2-y.get_width()//2,i*self.cell_size[1]+self.cell_size[1]//2-y.get_height()//2))
            for j in range(8):
                if (i + j) % 2 == 0:
                    colour = self.colours["white"]
                else:
                    colour = self.colours["black"]
                pygame.draw.rect(self.screen, colour, (i * self.cell_size[0]+self.axis_margin, j * self.cell_size[1], self.cell_size[0], self.cell_size[1]))
        if self.last_move:
            s = pygame.Surface((self.cell_size[0], self.cell_size[1]))
            s.set_alpha(128)
            s.fill((255,255,0))
            self.screen.blit(s, (self.last_move[1][0] * self.cell_size[0]+self.axis_margin, self.last_move[1][1] * self.cell_size[1]))
            s.fill((255,155,0))
            self.screen.blit(s, (self.last_move[0][0] * self.cell_size[0]+self.axis_margin, self.last_move[0][1] * self.cell_size[1]))
        for i in range(8):
            for j in range(8):
                if self.board.get((i,j)) and self.selected == (i,j):
                    for move in self.board[self.selected].calculate_moves(self.board, self.selected):
                        if move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7:
                            continue
                        s = pygame.Surface((self.cell_size[0], self.cell_size[1]))
                        s.set_alpha(128)
                        s.fill((255,0,0))
                        self.screen.blit(s, (move[0]*self.cell_size[0]+self.axis_margin, move[1]*self.cell_size[1]))
        
        for i in range(8):
            for j in range(8):
                if self.board.get((i,j)):
                    piece = self.board.get((i,j)).char
                    x = piece_font.render(piece, True, (0,0,0))
                    if self.selected == (i,j):
                        # draw selected piece at mouse
                        if self.board[(i,j)].type == "Knight" and self.board[(i,j)].index == 1:
                            x = pygame.transform.flip(x, True, False)
                        self.screen.blit(x, (pygame.mouse.get_pos()[0]-x.get_width()//2, pygame.mouse.get_pos()[1]-x.get_height()//2))
                    else:
                        if self.board[(i,j)].type == "Knight" and self.board[(i,j)].index == 1:
                            x = pygame.transform.flip(x, True, False)
                        self.screen.blit(x, (self.axis_margin+i*self.cell_size[0]+self.cell_size[0]//2-x.get_width()//2, j*self.cell_size[1]+self.cell_size[1]//2-x.get_height()//2))
        pygame.display.update()

    def main_loop(self):
        self.clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    # find which square the user clicked
                    x = (pos[0]-self.axis_margin) // self.cell_size[0]
                    y = (pos[1]) // self.cell_size[1]

                    x, y = int(x), int(y)

                    if self.board.get((x,y)) and self.board[(x,y)].colour == self.turn % 2:
                        self.selected = (x,y) if x > -1 and y < 8 and x < 8 and y > -1 else None
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.board.get(self.selected):
                        pos = pygame.mouse.get_pos()
                        # find which square the user clicked
                        x = (pos[0]-self.axis_margin) // self.cell_size[0]
                        y = (pos[1]) // self.cell_size[1]

                        if self.board[self.selected].colour == self.turn % 2 and (x,y) in self.board[self.selected].calculate_moves(self.board, self.selected) and x > -1 and y < 8 and x < 8 and y > -1: 
                            self.board[(x,y)] = self.board.pop(self.selected)
                            self.last_move = (self.selected, (x,y))
                            self.turn += 1

                        self.selected = None

            self.draw_board()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game(600)
    game.main_loop()

#     ♜	♞	♝	♛	♚	♝	♞	♜
# 7	♟	♟	♟	♟	♟	♟	♟	♟
# 6	



# ♙	♙	♙	♙	♙	♙	♙	♙
# ♖	♘	♗	♕	♔	♗	♘	♖
