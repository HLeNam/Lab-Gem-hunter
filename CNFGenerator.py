from abc import ABC, abstractmethod

from GemHunterGrid import GemHunterGrid


class CNFGenerator(ABC):
    def __init__(self, grid: GemHunterGrid):
        self.grid = grid
        self.rows = grid.rows
        self.cols = grid.cols
        self.clauses = []

    def position_to_variable(self, row, col):
        return row * self.cols + col + 1

    @abstractmethod
    def generate_exactly_n_clauses(self, neighbors, n):
        pass

    def generate_cnf(self):
        self.clauses = []
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.grid.grid[i][j]

                if isinstance(cell, int):
                    traps = cell
                    neighbors = self.grid.get_neighbors(i, j)

                    clauses = self.generate_exactly_n_clauses(neighbors, traps)
                    self.clauses.extend(clauses)

                elif cell == "T":
                    self.clauses.append([self.position_to_variable(i, j)])

                elif cell == "G":
                    self.clauses.append([-self.position_to_variable(i, j)])

        return self.remove_duplicate_clauses()

    def remove_duplicate_clauses(self):
        unique_clauses = []
        visited = set()

        for clause in self.clauses:
            clause_tuple = tuple(sorted(clause))
            if clause_tuple not in visited:
                visited.add(clause_tuple)
                unique_clauses.append(clause)

        return unique_clauses