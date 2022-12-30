# tetris_game.py



import pygame
import tetris_logic


TICK_RATE = 30
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 810
BACKGROUND_COLOR = pygame.Color(0, 0, 0)
OUTLINE_COLOR = pygame.Color(80, 80, 80)
COLORS = {
    "I": pygame.Color(143, 255, 255),
    "J": pygame.Color(143, 143, 255),
    "L": pygame.Color(255, 195, 143),
    "T": pygame.Color(210, 143, 255),
    "S": pygame.Color(143, 255, 156),
    "Z": pygame.Color(255, 143, 143),
    "O": pygame.Color(255, 255, 143),
    " ": pygame.Color(0, 0, 0)
}


class TetrisGame:

    def __init__(self) -> None:
        self._tick_counter = 0
        self._running = True
        self._board = tetris_logic.TetrisBoard()


    def run(self) -> None:

        pygame.init()

        try:
            clock = pygame.time.Clock()

            self._create_surface((SCREEN_WIDTH, SCREEN_HEIGHT))

            while self._running and self._board.game_running():

                clock.tick(TICK_RATE)

                self._tick_counter+= 1

                self._handle_events()
                self._display_frame()

                if self._tick_counter >= TICK_RATE:
                    self._tick_counter = 0
                    self._board._update()
                    self._board.print_board()
                    print()
                


        finally:
            pass

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.VIDEORESIZE:
                self._create_surface(event.size)
            elif event.type == pygame.KEYDOWN:
                if not self._board.has_piece():
                    continue
                if event.key == pygame.K_DOWN:
                    self._board.drop_piece()
                elif event.key == pygame.K_RIGHT:
                    self._board.move_piece_right()
                elif event.key == pygame.K_LEFT:
                    self._board.move_piece_left()
                elif event.key == pygame.K_z:
                    self._board.rotate_piece_left()
                elif event.key == pygame.K_x:
                    self._board.rotate_piece_right()
                elif event.key == pygame.K_SPACE:
                    self._board.full_drop()
                

    def _display_frame(self) -> None:

        self._surface.fill(BACKGROUND_COLOR)
        self._draw_board()
        pygame.display.flip()

    
    def _draw_board(self) -> None:
        surface_size = self._surface.get_size()
        if ((surface_size[0] // 10) > (surface_size[1] // 20)):
            square_size = surface_size[1] // 20
        else:
            square_size = surface_size[0] // 10

        self._draw_outline(square_size)
        self._draw_contents(square_size)

    def _draw_outline(self, square_size: int) -> None:
        pygame.draw.rect(self._surface, OUTLINE_COLOR, pygame.Rect(
            (self._surface.get_size()[0] - (square_size * 10)) // 2,
            (self._surface.get_size()[1] - (square_size * 20)) // 2,
            square_size * 10,
            square_size * 20
        ))
        pass

    def _draw_contents(self, square_size: int) -> None:
        for column in range(self._board.get_columns()):
            for row in range(self._board.get_rows()):
                color = COLORS.get(self._board.get_board()[column][row].get_piece())
                pygame.draw.rect(self._surface, color, pygame.Rect(
                    (self._surface.get_size()[0] - (square_size * 10)) // 2 + (square_size * (column + 0.1)),
                    (self._surface.get_size()[1] - (square_size * 20)) // 2 + (square_size * (row + 0.1)),
                    square_size * 0.8,
                    square_size * 0.8
                ))


    def _create_surface(self, size: tuple[int, int]) -> None:
        self._surface = pygame.display.set_mode((size[0], size[1]), pygame.RESIZABLE)


if __name__ == "__main__":
    TetrisGame().run()