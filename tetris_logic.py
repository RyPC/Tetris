# tetris_logic.py


import random


PIECES = "I", "J", "L", "T", "S", "Z", "O"
SQUARE_TYPES = "EMPTY", "PIECE", "FROZEN"
SHAPES = {
    "I": [  [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0]],

    "J": [  [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0]],

    "L": [  [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0]],

    "T": [  [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0]],

    "S": [  [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0]],
    
    "Z": [  [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0]],

    "O": [  [1, 1],
            [1, 1]]
}

COLUMNS = 10
ROWS = 20


class TetrisSquare:
    def __init__(self, piece: str, square_type = str) -> None:
        self._piece = piece
        self._square_type = square_type

    def is_empty(self) -> bool:
        """
        Returns if the square is "empty"
        """

        return self._piece == " "

    def is_piece(self) -> bool:
        """
        Returns if the piece is part of a falling piece
        """

        return self._square_type == "PIECE"
    
    def get_piece(self) -> str:
        """
        Returns the piece contents in string value
        """

        return self._piece

    def get_square_type(self) -> str:
        """
        Returns the type of square in string value:
            "EMPTY", "PIECE", "FROZEN"
        """

        return self._square_type




class TetrisPiece:
    def __init__(self, piece: str) -> None:
        self._piece = piece
        self._landed = False
        # number of clockwise rotations
        self._rotation = 0
        self._set_boundaries()


    def _set_boundaries(self) -> None:
        """
        Sets the initial boundaries of the piece boundary 
        """

        match(self._piece):
            case "I":
                self._top_left_bound = [-2, 3]
            case "O":
                self._top_left_bound = [0, 4]
            case _:
                self._top_left_bound = [0, 3]

    
    def get_rotated_shape(self) -> list[list[int]]:
        """
        Returns the piece's rotated shape in a matrix of 1's and 0's
        """
        shape = SHAPES.get(self._piece)

        for _ in range(self._rotation % 4):
            shape = self._rotate_shape(shape)

        return shape

    def _rotate_shape(self, shape: list[list[int]]) -> list[list[int]]:
        """
        Returns the piece's shape rotated once in a matrix of 1's and 0's
        """

        rotated_shape = []
        original_shape = shape

        for column in range(len(original_shape)):
            rotated_row = []
            for row in reversed(range(len(original_shape))):
                rotated_row.append(original_shape[row][column])
            rotated_shape.append(rotated_row)
        return rotated_shape

    def get_square_positions(self) -> list[tuple[int]]:
        """
        Returns a tuple with the coordinates of each of the solid squares in the piece
        """

        shape = self.get_rotated_shape()

        square_positions = []
        base_position = self._top_left_bound
        # shape = SHAPES.get(self._piece)

        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j] == 1:
                    square_positions.append((i + base_position[0], j + base_position[1]))
        return square_positions

    def get_piece(self) -> str:
        return self._piece

    def drop(self, squares = 1) -> None:
        self._top_left_bound[0]+= squares

    def rise(self, squares = 1) -> None:
        self._top_left_bound[0]-= squares

    def move_left(self, squares = 1) -> None:
        self._top_left_bound[1]-= squares

    def move_right(self, squares = 1) -> None:
        self._top_left_bound[1]+= squares

    def rotate_left(self) -> None:
        self._rotation-= 1
    
    def rotate_right(self) -> None:
        self._rotation+= 1

    def is_landed(self) -> bool:
        return self._landed

    def land(self) -> None:
        self._landed = True
    
    def unland(self) -> None:
        self._landed = False




class TetrisBoard:
    def __init__(self) -> None:
        self._game_running = True
        self._piece = None
        self._rows = ROWS
        self._columns = COLUMNS
        self._board = self._new_board()
        # self._create_new_piece()


    def _new_board(self) -> None:
        """
        Returns a new 2d array of "empty" TetrisSquare's
        """

        board = []
        for column in range(self._columns):
            empty_column = []
            for row in range(self._rows):
                empty_column.append(TetrisSquare(" "))
            board.append(empty_column)
        return board

    def _update(self) -> None:
        """
        Simulates a game tick and does ONE of the following:
            Creates a new falling piece
            Drops the falling piece one square
        """

        self._remove_piece_from_board()

        if not self.has_piece():
            # add new falling piece
            self._create_new_piece()
            self._add_piece_to_board()
            return

        # drop falling piece
        if self.piece_can_fall():
            self.drop_piece()
            if self.piece_can_fall():
                self._piece.unland()
        else:
            if self._piece.is_landed():
                self._freeze_piece()
                self._clear_rows()
                self._create_new_piece()
            else:
                self._piece.land()

        
        self._add_piece_to_board()


    def _update_pieces(self) -> None:
        self._remove_piece_from_board()
        self._add_piece_to_board()

    def _remove_piece_from_board(self) -> None:
        for column in range(self._columns):
            for row in range(self._rows):
                if self._board[column][row].is_piece():
                    self._board[column][row] = TetrisSquare(" ", "EMPTY")

    def _add_piece_to_board(self) -> None:
        for position in self._piece.get_square_positions():
            self._board[position[1]][position[0]] = TetrisSquare(self._piece.get_piece(), "PIECE")


    def _freeze_piece(self) -> None:
        for position in self._piece.get_square_positions():
            self._board[position[1]][position[0]] = TetrisSquare(self._piece.get_piece(), "FROZEN")
        self._piece = None
                

    
    def _create_new_piece(self) -> None:
        """
        Creates a new random piece and checks if the piece collides with current squares
        """

        self._piece = TetrisPiece(random.choice(PIECES))

        for position in self._piece.get_square_positions():
            if not self._board[position[1]][position[0]].is_empty():
                self._game_running = False


    def _clear_rows(self) -> None:
        for row in range(self._rows):
            for column in range(self._columns):
                if self._board[column][row].get_square_type() != "FROZEN":
                    break
            else:
                # row is completely FROZEN
                for column in range(self._columns):
                    del self._board[column][row]
                    self._board[column].insert(0, TetrisSquare(" ", "EMPTY"))


    def get_board(self) -> list[list[TetrisSquare]]:
        """
        Returns the instances board(2d array)
        """

        return self._board    

    def get_rows(self) -> int:
        """
        Returns the number of rows in the board
        """

        return self._rows

    def get_columns(self) -> int:
        """
        Returns the number of columns in the board
        """

        return self._columns


    def print_board(self) -> None:
        """
        Prints the board to the console separating pieces by "|"
        """

        # if self.has_piece():
        #     square_positions = self._piece.get_square_positions()
        # else:
        #     square_positions = []

        for row in range(self._rows):
            print("|", end = "")
            for column in range(self._columns):
                # if ((row, column) in square_positions):
                #     print(self._piece.get_piece(), end = "|")
                # else:
                    print(self._board[column][row].get_piece(), end = "|")
            print("|")

    def has_piece(self) -> bool:
        """
        Returns if the board has a valid falling piece
        """

        return self._piece != None


    def piece_can_fall(self) -> bool:
        """
        Returns if the piece can go down one square
        """

        self._piece.drop()
        can_fall = self._piece_in_valid_position()
        self._piece.rise()

        return can_fall

    def piece_can_left(self) -> bool:
        """
        Returns if the piece can move left one square
        """

        self._piece.move_left()
        can_left = self._piece_in_valid_position()
        self._piece.move_right()
        
        return can_left

    def piece_can_right(self) -> bool:
        """
        Returns if the piece can move right one square
        """

        self._piece.move_right()
        can_right = self._piece_in_valid_position()
        self._piece.move_left()

        return can_right

    def piece_can_rotate_right(self) -> bool:
        """
        Returns if the piece can rotate right
        """

        self._piece.rotate_right()
        can_rotate_right = self._piece_in_valid_position()
        self._piece.rotate_left()

        return can_rotate_right

    def piece_can_rotate_left(self) -> bool:
        """
        Returns if the piece can rotate left
        """

        self._piece.rotate_left()
        can_rotate_left = self._piece_in_valid_position()
        self._piece.rotate_right()

        return can_rotate_left

    def _piece_in_valid_position(self) -> bool:
        for position in self._piece.get_square_positions():
            if not (0 <= position[1] < self._columns and 0 <= position[0] < self._rows):
                return False
            if self._board[position[1]][position[0]].get_square_type() == "FROZEN":
                return False
        return True


    def move_piece_right(self) -> None:
        if self.piece_can_right():
            self._piece.move_right()
            self._update_pieces()

    def move_piece_left(self) -> None:
        if self.piece_can_left():
            self._piece.move_left()
            self._update_pieces()

    def rotate_piece_right(self) -> None:
        for i in range(3):
            for j in range(i + 1):
                for direction in (-1, 1):
                    self._piece.rise(i * direction)
                    self._piece.move_right(j * direction)

                    if self.piece_can_rotate_right():
                        self._piece.rotate_right()
                        self._update_pieces()
                        return

                    self._piece.drop((i + j) * direction)
                    self._piece.move_left((j - i) * direction)

                    if self.piece_can_rotate_right():
                        self._piece.rotate_right()
                        self._update_pieces()
                        return
                        
                    self._piece.move_left(i * direction)
                    self._piece.rise(j * direction)



    def rotate_piece_left(self) -> None:
        for i in range(3):
            for j in range(i + 1):
                for direction in (-1, 1):
                    self._piece.rise(i * direction)
                    self._piece.move_left(j * direction)
                    
                    if self.piece_can_rotate_left():
                        self._piece.rotate_left()
                        self._update_pieces()
                        return

                    self._piece.drop((i + j) * direction)
                    self._piece.move_right((j - i) * direction)

                    if self.piece_can_rotate_left():
                        self._piece.rotate_left()
                        self._update_pieces()
                        return
                        
                    self._piece.move_right(i * direction)
                    self._piece.rise(j * direction)
    

    def drop_piece(self) -> None:
        if self.piece_can_fall():
            self._piece.drop()
            self._remove_piece_from_board()
            self._add_piece_to_board()

    def full_drop(self) -> None:
        while self.piece_can_fall():
            self.drop_piece()
        self._remove_piece_from_board()
        self._freeze_piece()
        self._clear_rows()
        self._create_new_piece()
        self._add_piece_to_board()

        
    def game_running(self) -> bool:
        return self._game_running



if __name__ == "__main__":
    def prompt_input():
        input()

    board = TetrisBoard()
    board.print_board()
    
    while board.game_running():
        prompt_input()
        board._update()
        board.print_board()
        # print(board.piece_can_fall())
        print(SHAPES.get(board._piece._piece))