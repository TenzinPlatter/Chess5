import Globals as G

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

def collides_with_piece(x: int, y: int , pieces_list: list[Piece]) -> Piece | None:
    for piece in pieces_list:
        if piece.x == x and piece.y == y:
            return piece
    return None

def clone_piece(piece: Piece):
    #TODO keep function updated for when pieces get new properties
    if piece.piece_type == "pawn":
        new_piece = Pawn(piece.x, piece.y, piece.colour)
        new_piece.has_moved = piece.has_moved
        new_piece.valid_moves = piece.valid_moves

    if piece.piece_type == "rook":
        new_piece = Rook(piece.x, piece.y, piece.colour)
        new_piece.valid_moves = piece.valid_moves

    if piece.piece_type == "knight":
        new_piece = Knight(piece.x, piece.y, piece.colour)
        new_piece.valid_moves = piece.valid_moves

    if piece.piece_type == "bishop":
        new_piece = Bishop(piece.x, piece.y, piece.colour)
        new_piece.valid_moves = piece.valid_moves

    if piece.piece_type == "queen":
        new_piece = Queen(piece.x, piece.y, piece.colour)
        new_piece.valid_moves = piece.valid_moves

    if piece.piece_type == "king":
        new_piece = King(piece.x, piece.y, piece.colour)
        new_piece.valid_moves = piece.valid_moves
        new_piece.in_check = piece.in_check
        new_piece.has_moved = piece.has_moved
        new_piece.in_checkmate = piece.in_checkmate
        new_piece.in_stalemate = piece.in_stalemate
    return new_piece

def clone_pieces_list(pieces_list: list[Piece]) -> list[Piece]:
    result = []
    for piece in pieces_list:
        result.append(clone_piece(piece))
    return result

class Pieces:
    def __init__(self, pieces = None):
        if pieces is not None: 
            self.pieces = pieces
        else:
            self.pieces = init_array()
        self.set_all_valid_moves()

    def render_all(self, window):
        for piece in self.pieces:
            window.blit(piece.image, piece.image_pos)
    
    def get_piece_at(self, coords: tuple[int], pieces = None) -> Piece | None:
        x, y = coords
        if pieces is None: pieces = self.pieces
        for piece in pieces:
            if piece.x == x and piece.y == y:
                return piece
        return None
    
    def set_all_valid_moves(self):
        for piece in self.pieces:
            piece.set_valid_moves(self.pieces)
        self.filter_illegal_moves()

    def filter_illegal_moves(self):
        for piece in self.pieces:
            for move in piece.valid_moves:
                if self.move_is_illegal(piece, move):
                    piece.valid_moves.remove(move)
    
    def move_is_illegal(self, piece: Piece, move: list[int]) -> bool:
        temp_pieces = Pieces(pieces = self.pieces.copy())
        temp_pieces.pieces = clone_pieces_list(self.pieces)
        temp_piece = self.get_piece_at(( piece.x, piece.y ), pieces = temp_pieces.pieces)
        for piece in temp_pieces.pieces:
            piece.set_valid_moves(temp_pieces.pieces) 
        friendly_colour = temp_piece.colour
        for piece in temp_pieces.pieces:
            if piece.colour != friendly_colour or piece.piece_type != "king":
                friendly_king = piece
                break
        for piece in temp_pieces.pieces:
            for move in piece.valid_moves:
               if ( friendly_king.x == move[0] and friendly_king.y == move[1] ) and piece.colour != friendly_colour:
                   return True 
        return False
    
    def move_piece(self, piece: Piece, move: list[int]):
        if move not in self.valid_moves: raise Exception(f"Invalid move, {move} not in {self.valid_moves}")
        taken_piece = self.get_piece_at(move)
        self.x, self.y = move
        self.image_pos = G.coord_to_image_pos(move)
        if taken_piece is not None:
            self.pieces_class.pieces.remove(taken_piece)
        try:
            piece.has_moved = True
        except: 
            pass 

class Base_Piece_Methods:    
    def __init__(self, colour: str, x: int, y: int, piece_type: str):
        self._colour = colour
        self.x = x
        self.y = y
        self.piece_type = piece_type
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
                        valid_moves.append((x, y))
                    break
                valid_moves.append((x, y))
        self.valid_moves = valid_moves

    def is_valid_move(self, move: list[int]) -> bool:
        return move in self.valid_moves  


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
            valid_moves.append((x, y))
        for vector in take_vectors:
            x = self.x + vector[X]
            y = self.y + vector[Y]
            if x < 0 or x > 7 or y < 0 or y > 7:
                continue
            collided_piece = collides_with_piece(x, y, pieces_array)
            if collided_piece is not None and collided_piece.colour != self.colour:
                valid_moves.append((x, y))
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
            valid_moves.append((x, y))
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
        self.has_moved = False
        self.in_check = False
        self.in_checkmate = False
        self.in_stalemate = False


    def set_valid_moves(self, pieces_array: list[Piece]) -> list[tuple[int]]:
        X = 0
        Y = 1
        valid_moves = []
        for vector in self.valid_move_vectors:
            x = self.x + vector[X]
            y = self.y + vector[Y]
            out_of_bounds = ( x < 0 or x > 7 or y < 0 or y > 7 ) 
            collided_piece = collides_with_piece(x, y, pieces_array)
            occupied_by_friendly = (collided_piece is not None and collided_piece.colour == self.colour) 
            if out_of_bounds or occupied_by_friendly:
                continue
            valid_moves.append((x, y))
        self.valid_moves = valid_moves
