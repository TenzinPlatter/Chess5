import pygame
from Board import Board
from Piece import Pieces
import Globals

class App():
    def __init__(self) -> None:
        pygame.init()
        self.board = Board()
        self.pieces_class = Pieces()
        self._selected = None
        self.running = True
        self.window = pygame.display.set_mode((Globals.WIDTH, Globals.HEIGHT))
        self.clock = pygame.time.Clock()
        self.selected_piece = None
        self._white_turn = True
        self.move_made = False
        self.main_loop()

    @property
    def squares(self) -> list: return self._board.squares
    @property
    def pieces_list(self) -> list: return self.pieces_class.pieces
    @property
    def white_turn(self) -> bool: return self._white_turn
    @white_turn.setter
    def white_turn(self, value): 
        if value in [True, False]: self._white_turn = value
        else: raise Exception(f"{value} is not True or False")
    @property 
    def correct_turn(self) -> bool: 
        if (self.white_turn and self.selected_piece.colour == "white") or (not self.white_turn and self.selected_piece.colour == "black"): return True

    def main_loop(self) -> None:
        FPS = 60
        while self.running:
            if self.move_made:
                self.pieces_class.set_all_valid_moves()
                self.white_turn = not self.white_turn
                self.move_made = False
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
        if pygame.mouse.get_pressed()[LMB]:
            self.handle_left_click()
        if pygame.mouse.get_pressed()[RMB]:
            self.handle_right_click()

    def handle_left_click(self) -> None:
        if not Globals.can_select(): return
        coords = Globals.pos_to_coords(pygame.mouse.get_pos())
        x, y = coords
        if coords is None: return 
        piece = self.pieces_class.get_piece_at(coords)
        if self.selected_piece is not None and self.selected_piece.is_valid_move(coords) and self.correct_turn:
            self.selected_piece.move(coords)
            self.selected_piece = None
            self.move_made = True
            return
        if piece is None:
            self.board.unselect_all()
            self.selected_piece = piece
            return
        self.selected_piece = piece
        
    def handle_right_click(self) -> None:
        if not Globals.can_select(): return
        coords = Globals.pos_to_coords(pygame.mouse.get_pos())
        x, y = coords
        if coords is None: return
        self.squares[x][y].clicked_square()

    def render(self) -> None:
        self.board.render_all(self.window)
        self.pieces_class.render_all(self.window)
        self.render_selected_piece_moves()
        pygame.display.update()

    def render_selected_piece_moves(self):
        if self.selected_piece is None or not self.correct_turn: return
        for move in self.selected_piece.valid_moves:
            Globals.RenderCircle(move[0], move[1]).draw(self.window)


App()