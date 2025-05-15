class GemHunterGrid:
    def __init__(self, rows=0, cols=0, grid=None):
        self.rows = rows
        self.cols = cols
        if grid is None:
            self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        else:
            self._assign_grid(grid)

    def load_grid_from_file(self, filepath):
        try:
            with open(filepath, 'r') as file:
                lines = file.readlines()

            grid = []
            for line in lines:
                row = []
                cells = line.strip().split(",")
                for cell in cells:
                    cell = cell.strip()
                    if cell == "_":
                        row.append(cell)
                    else:
                        row.append(int(cell))
                grid.append(row)

            self._assign_grid(grid)
        except Exception as e:
            print(f"Error loading grid from file: {e}")
        finally:
            return self

    def _assign_grid(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0

    def save_grid_to_file(self, filepath):
        try:
            with open(filepath, 'w') as file:
                for row in self.grid:
                    line = ", ".join(str(cell) for cell in row)
                    file.write(line + "\n")
        except Exception as e:
            print(f"Error saving grid to file: {e}")

    def get_neighbors(self, row, col):
        neighbors = []
        for d_row in [-1, 0, 1]:
            for d_col in [-1, 0, 1]:
                if d_row == 0 and d_col == 0:
                    continue
                n_row = row + d_row
                n_col = col + d_col
                if 0 <= n_row < self.rows and 0 <= n_col < self.cols:
                    neighbors.append((n_row, n_col))

        return neighbors

    def __str__(self):
        grid_str = ""
        for row in self.grid:
            grid_str += ", ".join(str(cell) for cell in row) + "\n"
        return grid_str.strip()

    def clone(self):
        return GemHunterGrid(self.rows, self.cols, [row[:] for row in self.grid])