import pygame
from Board import Board
from Piece import Pieces
import Globals

class App():
    def __init__(self) -> None:
        pygame.init()
        self.board = Board()
        self.pieces = Pieces()
        self.selected = None
        self.running = True
        self.window = pygame.display.set_mode((Globals.WIDTH, Globals.HEIGHT))

        self.main_loop()

    def main_loop(self) -> None:
        while self.is_running():
            self.render()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

        pygame.quit()

    def render(self) -> None:
        self.get_board().render_all(self.window)
        self.get_pieces_class().render_all(self.window)
        pygame.display.update()

    def is_running(self) -> bool:
        return self.running
    def get_board(self) -> Board:
        return self.board
    def get_squares(self) -> list:
        return self.board.get_squares()
    def get_pieces_list(self) -> list:
        return self.pieces.get_pieces()
    def get_pieces_class(self) -> Pieces:
        return self.pieces
    
App()