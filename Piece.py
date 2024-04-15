import Globals as g

class Piece: pass #for type hinting

def init_array():
    result = []
    
    for x in range(8):
        result.append(Pawn(x, 6, "white"))
        result.append(Pawn(x, 1, "black"))
    
    for x in range(2):
        result.append(Rook(x * 7, 7, "white"))
        result.append(Rook(x * 7, 0, "black"))
        result.append(Knight(x * 5 + 1, 7, "white"))
        result.append(Knight(x * 5 + 1, 0, "black"))
        result.append(Bishop(x * 3 + 2, 7, "white"))
        result.append(Bishop(x * 3 + 2, 0, "black"))
    
    result.append(Queen(3, 7, "white"))
    result.append(Queen(3, 0, "black"))
    result.append(King(4, 7, "white"))
    result.append(King(4, 0, "black"))
    
    return result

def collides_with_piece(piece_to_check: Piece, pieces_list: list[Piece]) -> Piece | None:
    for piece in pieces_list:
        if piece.get_x() == piece_to_check.get_x() and piece.get_y() == piece_to_check.get_y():
            return piece
    return None


class Pieces:
    def __init__(self):
        self.pieces = init_array()
        self.set_all_valid_moves()

    def get_pieces(self):
        return self.pieces

    def render_all(self):
        pass
    
    def get_piece_at(self, coords: tuple[int]) -> Piece | None:
        x, y = coords
        for piece in self.get_pieces():
            if piece.get_x() == x and piece.get_y() == y:
                return piece
        return None
    
    def set_all_valid_moves(self):
        for piece in self.get_pieces():
            piece.set_valid_moves(self.get_pieces())


class Base_Piece_Methods:    
    def __init__(self, colour: str, x: int, y: int, piece_type: str):
        self.colour = colour
        self.x = x
        self.y = y
        self.piece_type = piece_type
        self.image = g.get_piece_image(piece_type, colour)

    def set_valid_moves(self, pieces_array: list[Piece]):
        X = 0
        Y = 1
        valid_moves = []
        for vector in self.get_valid_move_vectors():
            collided_piece = collides_with_piece(self, pieces_array)
            x = self.get_x()
            y = self.get_y()
            while True:
                x += vector[X]
                y += vector[Y]
                if x < 0 or x > 7 or y < 0 or y > 7:
                    break
                if collided_piece is not None:
                    if collided_piece.get_colour() != self.get_colour():
                        valid_moves.append((x, y))
                    break
                valid_moves.append((x, y))
            self.valid_moves = valid_moves

    def get_colour(self):
        return self.colour
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_piece_type(self):
        return self.piece_type
    def get_image(self):
        return self.image
    def get_valid_moves(self):
        return self.valid_moves
    def get_valid_move_vectors(self):
        return self.valid_move_vectors
    

class Pawn(Base_Piece_Methods):
    def __init__(self, x: int, y: int, colour: str):
        super().__init__(colour, x, y, "pawn")
        self.has_moved = False
        self.valid_move_vectors = (
            (0,1) if colour == "white" else (0,-1),
            (0,2) if colour == "white" else (0,-2)
        )
    
    def set_valid_moves(self, pieces_array: list[Piece]) -> list[tuple[int]]:
        X = 0
        Y = 1
        valid_moves = []
        for vector in self.valid_move_vectors:
            x = self.get_x() + vector[X]
            y = self.get_y() + vector[Y]
            if x < 0 or x > 7 or y < 0 or y > 7:
                continue
            collided_piece = collides_with_piece(self, pieces_array)
            if collided_piece is not None and collided_piece.get_colour() == self.get_colour():
                continue
            valid_moves.append((self.x+vector[X], self.y+vector[Y]))
        return valid_moves

class Knight(Base_Piece_Methods):
    def __init__(self, x: int, y: int, colour: str):
        super().__init__(colour, x, y, "knight")
        self.valid_move_vectors = (
            (1,2),
            (2,1),
            (-1,2),
            (-2,1),
            (1,-2),
            (2,-1),
            (-1,-2),
            (-2,-1)
        )
    
    def set_valid_moves(self, pieces_array: list[Piece]) -> list[tuple[int]]:
        X = 0
        Y = 1
        valid_moves = []
        for vector in self.valid_move_vectors:
            x = self.get_x() + vector[X]
            y = self.get_y() + vector[Y]
            if x < 0 or x > 7 or y < 0 or y > 7:
                continue
            collided_piece = collides_with_piece(self)
            if collided_piece is not None and collided_piece.get_colour() == self.get_colour():
                    continue
            valid_moves.append((x, y))
        return valid_moves


class Bishop(Base_Piece_Methods):
    def __init__(self, x: int, y: int, colour: str):
        super().__init__(colour, x, y, "bishop")
        self.valid_move_vectors = (
            (1,1),
            (1,-1),
            (-1,1),
            (-1,-1)
        )


class Rook(Base_Piece_Methods):
    def __init__(self, x: int, y: int, colour: str):
        super().__init__(colour, x, y, "rook")
        self.valid_move_vectors = (
            (0,1),
            (0,-1),
            (1,0),
            (-1,0)
        )


class Queen(Base_Piece_Methods):
    def __init__(self, x: int, y: int, colour: str):
        super().__init__(colour, x, y, "queen")
        self.valid_move_vectors = (
            (0,1),
            (0,-1),
            (1,0),
            (-1,0),
            (1,1),
            (1,-1),
            (-1,1),
            (-1,-1)
        )


class King(Base_Piece_Methods):
    def __init__(self, x: int, y: int, colour: str):
        super().__init__(colour, x, y, "king")
        self.valid_move_vectors = (
            (0,1),
            (0,-1),
            (1,0),
            (-1,0),
            (1,1),
            (1,-1),
            (-1,1),
            (-1,-1)
        )
        self.has_moved = False
        self.in_check = False
        self.in_checkmate = False
        self.in_stalemate = False