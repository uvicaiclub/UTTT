# author: Nathan Pannell

class custom_bot:
    """
    1) Play 3 in a row to win cell
    2) Block 3 in a row for opponent
    """

    """ 
                Required Functions
    """

    def __init__(self, name: str = 'vixen'):
        self.name = name

    def move(self, board_dict: dict) -> tuple:
        """
        Currently implementing the 'complete line' and 'block line' heuristics
        """
        board_state = board_dict['board_state']  # 9x9 np.array. Player = +1, Opponent = -1, Open = 0.
        active_box = board_dict['active_box']  # (col, row) of active board, (-1, -1) means all boards
        valid_moves = board_dict['valid_moves']  # List of tuples

        # Find Heuristics
        line_completions = self.get_line_completions(board_state, active_box, 1)
        blocking_moves = self.get_line_completions(board_state, active_box, -1)

        # Evaluation based on heuristics
        if len(line_completions) > 0:
            # 'complete line' heuristic
            random_index = np.random.randint(len(line_completions))
            return line_completions[random_index]
        elif len(blocking_moves) > 0:
            # 'block line' heuristic
            random_index = np.random.randint(len(blocking_moves))
            return blocking_moves[random_index]
        else:
            # no heuristic, random move
            random_index = np.random.randint(len(valid_moves))
            return valid_moves[random_index]

    """
                Core Utility Functions
    """

    def get_mini_board(self, board_state: np.array, index: tuple) -> np.array:
        """
        9x9 -> 3x3 @ index
        """
        return board_state[3 * index[0]: 3 * index[0] + 3, 3 * index[1]: 3 * index[1] + 3]

    """
                Specific Heuristic Evaluations
    """

    def get_line_completions(self, board_state: np.array, active_board: tuple, target: int) -> [tuple]:
        """
        Finds active mini boards
        Gets line-completing moves on each mini board
        Target determines whether looking for player or opponent lines
        Returns a list of all unique moves (as tuples)
        """
        line_completing_moves = []

        if active_board == (-1, -1):  # Every board is active, loop through all
            for x in range(3):
                for y in range(3):
                    line_completing_moves += self.complete_line(board_state, (x, y), target)
        else:  # Specific active board
            line_completing_moves += self.complete_line(board_state, active_board, target)

        # Only want unique moves
        return [t for t in set(tuple(i) for i in line_completing_moves)]

    def complete_line(self, board: np.array, active_board: tuple, target: int) -> [tuple]:
        """
        Looks for patterns of [1, 1, 0] in a line (or [-1, -1, 0])
        Moves are in position of currently empty cells on these lines
        Return all possible 'line completing' moves
        """
        # Get relevant 3x3 board
        mini = self.get_mini_board(board, active_board)

        # Possible lines (written as 3x + y for conciseness)
        lines = ['012', '345', '678', '036', '147', '258', '048', '246']
        line_completing_moves = []
        for line in lines:  # For each line combination
            values = []
            for cell in line:  # For each cell in line
                # Unpacking value into col (x) and row (y)
                x = int(cell) // 3
                y = int(cell) % 3
                values.append(mini[x][y])  # Save value of cell

            if sum(values) == 2 * target:  # sum([1, 1, 0]) produces 2, so we found a play!
                i = values.index(0)  # Index of line-completing move within string
                x = int(line[i]) // 3
                y = int(line[i]) % 3
                line_completing_moves.append((x, y))

        # Convert moves to global scope and return
        return [(move[0] + 3 * active_board[0], move[1] + 3 * active_board[1]) for move in line_completing_moves]
