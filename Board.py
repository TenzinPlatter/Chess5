import pygame
import Globals as G
class index():
    pass

class Board():
    def __init__(self, squares = None) -> None:
        self._squares = Board.init_array()
        
    @property
    def squares(self) -> list: return self._squares
    
    def render_all(self, window: pygame.surface):
        for col in self.squares:
            for square in col:
                pygame.draw.rect(window, square.colour, square.rect)
    
    def unselect_all(self):
        for col in self.squares:
            for square in col:
                square.selected = True
                square.clicked_square()

    @staticmethod
    def init_array() -> list:
        final = []
        for x in range(8):
            col = []
            for y in range(8):
                if (x+y)%2==0:
                    col.append(Square(x, y, G.LIGHTCOLOUR))
                else:
                    col.append(Square(x, y, G.DARKCOLOUR))
            final.append(col)
        return final


class Square():
    def __init__(self, x: index, y: index, colour):
        self._colour = colour
        self._size = G.SQUARE_SIZE
        self._x = x
        self._y = y
        self._rect = pygame.Rect(*G.coord_to_pos((x, y)), G.SQUARE_SIZE, G.SQUARE_SIZE)
        self._selected = False
           
    def clicked_square(self) -> None:
        if self.selected:
            if (self.x+self.y)%2==0:
                self.colour = G.LIGHTCOLOUR
            else:
                self.colour = G.DARKCOLOUR
        else:
            self.colour = G.SELECTEDCOLOUR
        self.selected = not self.selected

    @property
    def rect(self): return self._rect
    @rect.setter
    def rect(self, new_rect): self._rect = new_rect
    @property
    def colour(self): return self._colour
    @colour.setter
    def colour(self, new_colour): self._colour = new_colour
    @property
    def size(self): return self._size
    @size.setter
    def size(self, new_size): self._size = new_size
    @property
    def x(self): return self._x
    @x.setter
    def x(self, new_x): self._x = new_x
    @property
    def y(self): return self._y
    @y.setter
    def y(self, new_y): self._y = new_y
    @property
    def selected(self): return self._selected
    @selected.setter
    def selected(self, new_selected): self._selected = new_selected
