from abc import ABC, abstractmethod

class ICNFSolver(ABC):
    def __init__(self, clauses, rows, cols, grid=None):
        self.clauses = clauses
        self.rows = rows
        self.cols = cols
        self.grid = grid if grid else [['_' for _ in range(cols)] for _ in range(rows)]

    def position_to_var(self, i, j):
        return i * self.cols + j + 1

    def var_to_position(self, var):
        var = abs(var) - 1
        i = var // self.cols
        j = var % self.cols
        return i, j

    @abstractmethod
    def solve(self):
        pass

    def create_result_grid(self, model):
        result_grid = [['_' for _ in range(self.cols)] for _ in range(self.rows)]
        print("Original grid:", self.grid.grid)
        print("Result grid:", result_grid)

        for var in model:
            i, j = self.var_to_position(var)

            if i < 0 or i >= self.rows or j < 0 or j >= self.cols:
                continue

            # Nếu biến dương, tức là ô chứa bẫy
            if var > 0:
                result_grid[i][j] = 'T'
            # Nếu biến âm, tức là ô chứa đá quý
            elif var < 0:
                result_grid[i][j] = 'G'
                if type(self.grid.grid[i][j]) == int:
                    result_grid[i][j] = self.grid.grid[i][j]

        # Nếu ô không chứa bẫy hoặc đá quý, giữ nguyên giá trị
        for i in range(self.rows):
            for j in range(self.cols):
                if result_grid[i][j] == '_':
                    result_grid[i][j] = self.grid.grid[i][j]

        return result_grid