import pygame
from Board import Board
from Piece import Pieces
import Globals

class App():
    def __init__(self) -> None:
        pygame.init()
        self._board = Board()
        self._pieces_class = Pieces()
        self._selected = None
        self._running = True
        self._window = pygame.display.set_mode((Globals.WIDTH, Globals.HEIGHT))
        self.clock = pygame.time.Clock()
        self.main_loop()

    @property
    def running(self) -> bool: return self._running
    @running.setter
    def running(self, value: bool) -> None: self._running = value
    @property
    def board(self) -> Board: return self._board
    @property
    def squares(self) -> list: return self._board.squares
    @property
    def pieces_list(self) -> list: return self.pieces_class.pieces
    @property
    def pieces_class(self) -> Pieces: return self._pieces_class
    @property
    def window(self) -> pygame.surface: return self._window

    def main_loop(self) -> None:
        FPS = 60
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.render()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        LMB = 0
        RMB = 2
        #TODO make sure there is no issue with processing lmb and rmb in one frame
        if pygame.mouse.get_pressed()[LMB]:
            self.handle_left_click()
        if pygame.mouse.get_pressed()[RMB]:
            self.handle_right_click()

    def handle_left_click(self) -> None:
        if not Globals.can_select(): return
        x, y = pygame.mouse.get_pos()
        coords = Globals.pos_to_coords((x, y))
        if coords is None: return 
        piece = self.pieces_class.get_piece_at(coords)
        if piece is None:
            self.board.unselect_all()
            return
        
    def handle_right_click(self) -> None:
        if not Globals.can_select(): return
        x, y = pygame.mouse.get_pos()
        coords = Globals.pos_to_coords((x, y))
        if coords is None: return
        piece = self.pieces_class.get_piece_at(coords)
        if piece is not None: pass #TODO show piece moves
        self.board.clicked_square(coords)

    def render(self) -> None:
        self.board.render_all(self.window)
        self.pieces_class.render_all(self.window)
        pygame.display.update()


    
App()