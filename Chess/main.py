from typing import Text
import pygame
from pieces import *

pygame.font.init()

class Game:
    def __init__(self, width, height) -> None:
        self.colours = {
            "black": (118,150,86),
            "white": (238,238,210),
        }

        self.width, self.height = width, height
        self.cell_size = (self.width // 8, self.height // 8)

        self.screen = pygame.display.set_mode((self.width+40+60, self.height+40))
        self.screen.fill((255, 255, 255))

        self.selected = None

        self.board = {
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
        }
    
    def draw_board(self):
        self.screen.fill(self.colours["black"])
        pygame.draw.line(self.screen, (0,0,0), (39,0), (39,self.height), 1)
        pygame.draw.line(self.screen, (0,0,0), (40,self.height), (self.width+40,self.height), 1)
        pygame.draw.line(self.screen, (0,0,0), (self.width+40,0), (self.width+40,self.height), 1)
        label_font = pygame.font.SysFont("Arial", 40)
        piece_font = pygame.font.Font("FreeSerif.otf", 72)
        for i in range(8):
            x = label_font.render(str(chr(i+65)), True, self.colours["white"])
            y = label_font.render(str(8-i), True, self.colours["white"])
            self.screen.blit(x, (40+i*self.cell_size[0]+self.cell_size[0]//2-x.get_width()//2, self.height+20-x.get_height()//2))
            self.screen.blit(y, (20-y.get_width()//2,i*self.cell_size[1]+self.cell_size[1]//2-y.get_height()//2))
            for j in range(8):
                if (i + j) % 2 == 0:
                    colour = self.colours["white"]
                else:
                    colour = self.colours["black"]
                pygame.draw.rect(self.screen, colour, (i * self.cell_size[0]+40, j * self.cell_size[1], self.cell_size[0], self.cell_size[1]))
        
        for i in range(8):
            for j in range(8):
                if self.board.get((i,j)):
                    piece = self.board.get((i,j)).char
                    x = piece_font.render(piece, True, (0,0,0))
                    if self.selected == (i,j):
                        # draw selected piece at mouse
                        self.screen.blit(x, (pygame.mouse.get_pos()[0]-x.get_width()//2, pygame.mouse.get_pos()[1]-x.get_height()//2))
                        for move in self.board[self.selected].calculate_moves(self.board, self.selected):
                            s = pygame.Surface((self.cell_size[0], self.cell_size[1]))
                            s.set_alpha(128)
                            s.fill((255,0,0) if not self.board.get(move) else (255,155,0))
                            self.screen.blit(s, (move[0]*self.cell_size[0]+40, move[1]*self.cell_size[1]))
                    else:
                        self.screen.blit(x, (40+i*self.cell_size[0]+self.cell_size[0]//2-x.get_width()//2, j*self.cell_size[1]+self.cell_size[1]//2-x.get_height()//2))
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
                    x = (pos[0]-40) // self.cell_size[0]
                    y = (pos[1]) // self.cell_size[1]

                    self.selected = (x,y) if x > -1 and y < 8 else None
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.board.get(self.selected):
                        pos = pygame.mouse.get_pos()
                        # find which square the user clicked
                        x = (pos[0]-40) // self.cell_size[0]
                        y = (pos[1]) // self.cell_size[1]

                        if (x,y) in self.board[self.selected].calculate_moves(self.board, self.selected): self.board[(x,y)] = self.board.pop(self.selected)

                        self.selected = None

            self.draw_board()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game(800, 800)
    game.main_loop()

#     ♜	♞	♝	♛	♚	♝	♞	♜
# 7	♟	♟	♟	♟	♟	♟	♟	♟
# 6	



# ♙	♙	♙	♙	♙	♙	♙	♙
# ♖	♘	♗	♕	♔	♗	♘	♖
