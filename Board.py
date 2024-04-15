import pygame
import Globals as G
class index():
    pass

class Board():
    def __init__(self) -> None:
        self.squares = Board.init_array()
    
    def render_all(self, window: pygame.surface):
        for col in self.get_squares():
            for square in col:
                pygame.draw.rect(window, square.colour, square.rect)
    
    def unselect_all(self):
        for col in self.get_squares():
            for square in col:
                square.unselect()

    def get_squares(self):
        return self.squares

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
        self.colour = colour
        self.size = G.SQUARE_SIZE
        self.x = x
        self.y = y
        self.rect = pygame.Rect(G.add_offest(x), G.add_offest(y), G.SQUARE_SIZE, G.SQUARE_SIZE)
        self.selected = False
        
    def unselect(self):
        if (self.x+self.y)%2==0:
            self.colour = G.LIGHTCOLOUR
        else:
            self.colour = G.DARKCOLOUR

    def select_square(self) -> None:
        if self.is_selected():
            self.unselect()
        else:
            self.colour = G.SELECTEDCOLOUR

    def get_rect(self):
        return self.rect
    def get_colour(self):
        return self.COLOUR
    def get_size(self):
        return self.size
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def is_selected(self):
        return self.selected