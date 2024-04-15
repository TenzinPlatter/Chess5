import pygame

WINSIZE = WIDTH, HEIGHT = (900,900)
BORDER = 50
SQUARE_SIZE = 100
LMB, RMB = 1,3
LIGHTCOLOUR = (245, 179, 113)
DARKCOLOUR = (168, 94, 20)
SELECTEDCOLOUR = (255, 51, 51)
VALIDCOLOUR = (160,160,160)
DELAY = 300
lastTime = 0
renderingQueue = []

dirVectors = {
    "rook":[[1,0],[-1,0],[0,1],[0,-1]],
    "bishop":[[1,1],[1,-1],[-1,1],[-1,-1]],
    "queen":[[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]],
    "king":[[1,0],[1,1],[1,-1],[-1,0],[-1,1],[-1,-1],[0,1],[0,-1]],
    "knight":[[2,1],[-2,-1],[2,-1],[-2,1],[1,2],[1,-2],[-1,-2],[-1,2]]
}

def can_select() -> bool:
    global lastTime
    if lastTime+DELAY>pygame.time.get_ticks():
        return False
    lastTime = pygame.time.get_ticks()
    return True

def pos_to_coords(coords: tuple[int]) -> tuple[int]:
    """Converts the x, y coordinates of the mouse to the x, y coordinates of the board."""
    x,y = coords
    x,y = int((x-BORDER)/SQUARE_SIZE), int((y-BORDER)/SQUARE_SIZE)
    if x<0 or x>7 or y<0 or y>7:
        return False
    return x,y

def coord_to_pos(coord) -> int:
    x, y = coord
    return x * SQUARE_SIZE + BORDER, y * SQUARE_SIZE + BORDER

def coord_to_image_pos(coords: tuple[int], corner_offset_from_center: float = 0) -> int:
    x, y = coords
    x = x * SQUARE_SIZE + BORDER + corner_offset_from_center
    y = y * SQUARE_SIZE + BORDER + corner_offset_from_center
    return x, y

def render_queue(surface) -> int:
    for item in renderingQueue:
        item.draw(surface)

def get_piece_image(name: str, colour: str) -> pygame.image:
    return pygame.transform.scale(pygame.image.load(f"Piece_Pngs/{name}_{colour}.png"), (SQUARE_SIZE, SQUARE_SIZE))

class RenderCircle():
    def __init__(self,x,y):
        self.center = (x+.5)*SQUARE_SIZE+BORDER, (y+.5)*SQUARE_SIZE+BORDER
    
    def draw(self, surf: pygame.surface) -> None:
        pygame.draw.circle(surf, VALIDCOLOUR, self.center, SQUARE_SIZE*.2)
        
