from pysat.solvers import Solver
import time

from CardinalityStrategy import CardinalityStrategy
from TruthTableStrategy import TruthTableStrategy


class GemHunterSolver:
    """Bộ giải cho bài toán Thợ săn đá quý có thể sử dụng nhiều chiến lược CNF khác nhau"""

    TRUTH_TABLE = "truth_table"
    CARDINALITY = "cardinality"

    def __init__(self, grid, strategy_name=CARDINALITY):
        """Khởi tạo bộ giải với một chiến lược cụ thể"""
        self.strategy = None
        self.grid = grid
        self.rows = grid.rows
        self.cols = grid.cols
        self.set_strategy(strategy_name)

    def set_strategy(self, strategy_name):
        """Thay đổi chiến lược tạo CNF"""
        if strategy_name == self.TRUTH_TABLE:
            self.strategy = TruthTableStrategy(self.grid)
        elif strategy_name == self.CARDINALITY:
            self.strategy = CardinalityStrategy(self.grid)
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")

    def position_to_var(self, i, j):
        """Chuyển đổi vị trí (i,j) thành biến CNF"""
        return i * self.cols + j + 1

    def var_to_position(self, var):
        """Chuyển đổi biến CNF thành vị trí (i,j)"""
        var = abs(var) - 1  # Trừ 1 vì biến CNF bắt đầu từ 1
        i = var // self.cols
        j = var % self.cols
        return i, j

    def solve(self):
        """Giải bài toán Thợ săn đá quý"""
        # Bắt đầu đo thời gian
        start_time = time.time()

        # Tạo CNF bằng chiến lược đã chọn
        cnf_clauses = self.strategy.generate_cnf()
        generation_time = time.time() - start_time

        print(f"Generated {len(cnf_clauses)} CNF clauses in {generation_time:.6f} seconds")

        # Giải CNF bằng PySAT
        solving_start_time = time.time()
        with Solver(name='g4') as solver:
            # Thêm tất cả các mệnh đề vào bộ giải
            for clause in cnf_clauses:
                solver.add_clause(clause)

            # Kiểm tra xem có giải pháp không
            if solver.solve():
                # Lấy mô hình (các giá trị cho các biến)
                model = solver.get_model()

                # Tạo lưới kết quả
                result_grid = [['_' for _ in range(self.cols)] for _ in range(self.rows)]

                # Lặp qua các biến trong mô hình
                for var in model:
                    i, j = self.var_to_position(var)

                    # Nếu biến dương, tức là ô chứa bẫy
                    if var > 0 and 0 <= i < self.rows and 0 <= j < self.cols:
                        result_grid[i][j] = 'T'
                    # Nếu biến âm, tức là ô chứa đá quý
                    elif var < 0 <= i < self.rows and 0 <= j < self.cols:
                        i, j = self.var_to_position(var)
                        print("Found gem at:", i, j, "with value:", self.grid.grid[i][j])
                        result_grid[i][j] = 'G'
                        if type(self.grid.grid[i][j]) == int:
                            result_grid[i][j] = str(self.grid.grid[i][j])

                solving_time = time.time() - solving_start_time
                total_time = time.time() - start_time

                # Trả về các thống kê
                stats = {
                    "success": True,
                    "clauses": len(cnf_clauses),
                    "generation_time": generation_time,
                    "solving_time": solving_time,
                    "total_time": total_time,
                    "result_grid": result_grid
                }

                return stats
            else:
                solving_time = time.time() - solving_start_time
                total_time = time.time() - start_time

                return {
                    "success": False,
                    "clauses": len(cnf_clauses),
                    "generation_time": generation_time,
                    "solving_time": solving_time,
                    "total_time": total_time,
                    "result_grid": None
                }