import random



import copy





class SudokuGenerator:


    """Generate Sudoku puzzles for both standard (1-9) and hex (0-F) variants."""


    


    def __init__(self, size=9):


        """


        Initialize generator.


        Args:


            size: Board size (9 for standard, 16 for hex)


        """


        self.size = size


        self.box_size = int(size ** 0.5)


        


    def generate_puzzle(self, difficulty='medium'):


        """


        Generate a complete Sudoku puzzle.


        Args:


            difficulty: 'easy', 'medium', or 'hard'


        Returns:


            2D list representing the puzzle


        """


        # Create a complete solved board


        board = self._create_solved_board()


        


        # Remove numbers based on difficulty


        puzzle = self._remove_numbers(board, difficulty)


        


        return puzzle


    


    def _create_solved_board(self):


        """Create a completely solved Sudoku board."""


        board = [[0 for _ in range(self.size)] for _ in range(self.size)]


        self._fill_board(board)


        return board


    


    def _fill_board(self, board, row=0, col=0):


        """Recursively fill the board using backtracking."""


        if row == self.size:


            return True


        


        next_row, next_col = (row, col + 1) if col + 1 < self.size else (row + 1, 0)


        


        numbers = list(range(1, self.size + 1))


        random.shuffle(numbers)


        


        for num in numbers:


            if self._is_valid(board, row, col, num):


                board[row][col] = num


                if self._fill_board(board, next_row, next_col):


                    return True


                board[row][col] = 0


        


        return False


    


    def _is_valid(self, board, row, col, num):


        """Check if placing num at (row, col) is valid."""


        # Check row


        if num in board[row]:


            return False


        


        # Check column


        if num in [board[r][col] for r in range(self.size)]:


            return False


        


        # Check box


        box_row, box_col = (row // self.box_size) * self.box_size, (col // self.box_size) * self.box_size


        for r in range(box_row, box_row + self.box_size):


            for c in range(box_col, box_col + self.box_size):


                if board[r][c] == num:


                    return False


        


        return True


    


    def _remove_numbers(self, board, difficulty):


        """Remove numbers from solved board based on difficulty."""


        puzzle = copy.deepcopy(board)


        


        # Define removal counts based on difficulty


        removal_map = {


            'easy': int(self.size * self.size * 0.4),    # 40% removed


            'medium': int(self.size * self.size * 0.5),  # 50% removed


            'hard': int(self.size * self.size * 0.6)     # 60% removed


        }


        


        removals = removal_map.get(difficulty, removal_map['medium'])


        


        positions = [(r, c) for r in range(self.size) for c in range(self.size)]


        random.shuffle(positions)


        


        for i in range(removals):


            row, col = positions[i]


            puzzle[row][col] = 0


        


        return puzzle








class HexSudokuGenerator(SudokuGenerator):


    """Generator for 16x16 hexadecimal Sudoku."""


    


    def __init__(self):


        super().__init__(size=16)


    


    def generate_puzzle(self, difficulty='medium'):


        """Generate hex Sudoku and convert to hex strings."""


        puzzle = super().generate_puzzle(difficulty)


        return self._convert_to_hex(puzzle)


    


    def _convert_to_hex(self, board):


        """Convert numeric board to hex representation."""


        hex_board = []


        for row in board:


            hex_row = []


            for cell in row:


                if cell == 0:


                    hex_row.append('0')


                else:


                    hex_row.append(format(cell, 'X'))


            hex_board.append(hex_row)


        return hex_board