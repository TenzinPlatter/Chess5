from re import M
import Globals as G
from dataclasses import dataclass
#TODO make sure pieces cannot jump over others

class Piece: pass #for type hinting

@dataclass
class Move:
    vector: tuple[int]
    start_coords: tuple[int]

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

def collides_with_piece(x: int, y: int , pieces_list: list[Piece]) -> Piece | None:
    for piece in pieces_list:
        if piece.x == x and piece.y == y:
            return piece
    return None


class Pieces:
    def __init__(self):
            self.pieces = init_array() 
            self.pieces.set_all_valid_moves(white_turn = True)

    def render_all(self, window):
        for piece in self.pieces:
            window.blit(piece.image, piece.image_pos)
    
    def get_piece_at(self, coords: tuple[int]) -> Piece | None:
        x, y = coords
        for piece in self.pieces:
            if piece.x == x and piece.y == y:
                return piece
        return None
    
    def set_all_valid_moves(self, white_turn):
        for piece in self.pieces:
            if self.is_white = white_turn:
                piece.set_valid_moves(self.pieces)

    def filter_valid_moves(self):
        """removes psuedo legal moves"""
        for piece in self.pieces:
            for move in piece.valid_moves:
                if self.move_is_illegal(piece, move):
                    piece.valid_moves.remove(move)

    def move_is_illegal(self, piece: Piece, move: tuple[int]) -> bool:
        temp_pieces = self.pieces.copy()
        for piece in temp_pieces:
            if piece.type == "king" and piece.colour == piece.colour:
                friendly_king = piece
                break


    def move_piece(self, selected_piece: Piece, move: Move):
        coords = move.start_coords
        taken_piece = self.get_piece_at(coords)
        selected_piece.move(coords)
        if taken_piece is not None:
            self.pieces.remove(taken_piece)
        


class Base_Piece_Methods:    
    def __init__(self, colour: str, x: int, y: int, piece_type: str):
        self._colour = colour
        self.is_white = colour == "white"
        self.x = x
        self.y = y
        self.type = piece_type
        self.image = G.get_piece_image(piece_type, colour)
        self.valid_move_vectors = None
        self.image_pos = G.coord_to_image_pos((x, y))
        self.valid_moves = []

    @property
    def colour(self): return self._colour
    @colour.setter
    def colour(self, value): raise Exception("Cannot change colour of piece")

    def set_valid_moves(self, pieces_array: list[Piece]):
        X = 0
        Y = 1
        valid_moves = []
        for vector in self.valid_move_vectors:
            x = self.x
            y = self.y
            while True:
                x += vector[X]
                y += vector[Y]
                collided_piece = collides_with_piece(x, y, pieces_array)
                if x < 0 or x > 7 or y < 0 or y > 7:
                    break
                if collided_piece is not None:
                    if collided_piece.colour != self.colour:
                        move = Move((x, y), (self.x, self.y))
                        valid_moves.append(move)
                    break
                move = Move((x, y), (self.x, self.y))
                valid_moves.append(move)
        self.valid_moves = valid_moves

    def set_valid_moves_skip_king(self, pieces_array):
        X = 0
        Y = 1
        valid_moves = []
        for vector in self.valid_move_vectors:
            x = self.x
            y = self.y
            while True:
                x += vector[X]
                y += vector[Y]
                collided_piece = collides_with_piece(x, y, pieces_array)
                if x < 0 or x > 7 or y < 0 or y > 7:
                    break
                if collided_piece is not None:
                    if collided_piece.colour != self.colour:
                        move = Move((x, y), (self.x, self.y))
                        valid_moves.append(move)
                    if collided_piece.piece_type == "king": 
                        continue
                    break
                move = Move((x, y), (self.x, self.y))
                valid_moves.append(move)
        self.valid_moves = valid_moves


    def is_valid_move(self, move: Move) -> bool:
        return move in self.valid_moves
    
    def get_move_with_coords(self, coords: tuple[int]) -> Move | None:
        for move in self.valid_moves:
            if move.vector == coords:
                return move

    def move(self, move: list[int]):
        if move not in self.valid_moves: raise Exception(f"Invalid move, {move} not in {self.valid_moves}")
        self.x, self.y = move
        self.image_pos = G.coord_to_image_pos(move)

class Pawn(Base_Piece_Methods):
    def __init__(self, x: int, y: int, colour: str):
        super().__init__(colour, x, y, "pawn")
        self._has_moved = False
        self.valid_move_vectors = (
            (0,-1) if colour == "white" else (0,1),
            (0,-2) if colour == "white" else (0,2)
        )
    
    def has_moved(self, value):
        if value is True:
            self.has_moved = value
            self.valid_move_vectors = ((0,-1) if self.colour == "white" else (0,1),)
    
    def set_valid_moves(self, pieces_array: list[Piece]) -> list[tuple[int]]:
        #TODO add en passant and fix pawn not having valid moves later in game
        X = 0
        Y = 1
        take_vectors = (
            (1, -1) if self.colour == "white" else (1, 1),
            (-1, -1) if self.colour == "white" else (-1, 1)
        )
        valid_moves = []
        for vector in self.valid_move_vectors:
            x = self.x + vector[X]
            y = self.y + vector[Y]
            collided_piece = collides_with_piece(x, y, pieces_array)
            if collided_piece is not None or x < 0 or x > 7 or y < 0 or y > 7:
                break
            move = Move((x, y), (self.x, self.y))
            valid_moves.append(move)
        for vector in take_vectors:
            x = self.x + vector[X]
            y = self.y + vector[Y]
            if x < 0 or x > 7 or y < 0 or y > 7:
                continue
            collided_piece = collides_with_piece(x, y, pieces_array)
            if collided_piece is not None and collided_piece.colour != self.colour:
                move = Move((x, y), (self.x, self.y))
                valid_moves.append(move)
        self.valid_moves = valid_moves

    def move(self, move: list[int]):
        if move not in self.valid_moves: raise Exception(f"Invalid move, {move} not in {self.valid_moves}")
        self.x, self.y = move
        self.image_pos = G.coord_to_image_pos(move)
        self.has_moved = True
        self.valid_move_vectors = (
            (0,-1) if self.colour == "white" else (0,1),
        )



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
    #TODO add move method 
    def set_valid_moves(self, pieces_array: list[Piece]) -> list[tuple[int]]:
        X = 0
        Y = 1
        valid_moves = []
        for vector in self.valid_move_vectors:
            x = self.x + vector[X]
            y = self.y + vector[Y]
            if x < 0 or x > 7 or y < 0 or y > 7:
                continue
            collided_piece = collides_with_piece(x, y, pieces_array)
            if collided_piece is not None and collided_piece.colour == self.colour:
                    continue
            move = Move((x, y), (self.x, self.y))
            valid_moves.append(move)
        self.valid_moves = valid_moves


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
        self._has_moved = False
        self._in_check = False
        self._in_checkmate = False
        self._in_stalemate = False

    @property
    def has_moved(self): return self._has_moved
    @has_moved.setter
    def has_moved(self, value):
        if value is True:
            self._has_moved = True
            #TODO add changes for after the king moves

    def set_valid_moves(self, pieces_array: list[Piece]) -> list[tuple[int]]:
        self.valid_moves = []
        for vector in self.valid_move_vectors:
            x = self.x + vector[0]
            y = self.y + vector[1]
            if x < 0 or x > 7 or y < 0 or y > 7:
                continue
            collided_piece = collides_with_piece(x, y, pieces_array)
            if collided_piece is not None and collided_piece.colour == self.colour:
                continue
            move = Move((x, y), (self.x, self.y))
            self.valid_moves.append(move)
    
