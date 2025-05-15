import time

from BacktrackingSolver import BacktrackingSolver
from BruteForceSolver import BruteForceSolver
from CardinalityStrategy import CardinalityStrategy
from PySATSolver import PySATSolver
from TruthTableStrategy import TruthTableStrategy

class GemHunterSolver:
    """Bộ giải cho bài toán Thợ săn đá quý có thể sử dụng nhiều chiến lược CNF và thuật toán giải khác nhau"""

    # Các chiến lược tạo CNF
    TRUTH_TABLE = "truth_table"
    CARDINALITY = "cardinality"

    # Các thuật toán giải CNF
    BRUTE_FORCE = "brute_force"
    BACKTRACKING = "backtracking"
    PYSAT = "pysat"

    def __init__(self, grid, cnf_strategy=CARDINALITY, solver_algorithm=PYSAT):
        """Khởi tạo bộ giải với một chiến lược CNF và thuật toán giải cụ thể"""
        self.cnf_strategy = None
        self.grid = grid
        self.rows = grid.rows
        self.cols = grid.cols
        self.set_cnf_strategy(cnf_strategy)
        self.solver_algorithm = solver_algorithm

    def set_cnf_strategy(self, strategy_name):
        """Thay đổi chiến lược tạo CNF"""
        if strategy_name == self.TRUTH_TABLE:
            self.cnf_strategy = TruthTableStrategy(self.grid)
        elif strategy_name == self.CARDINALITY:
            self.cnf_strategy = CardinalityStrategy(self.grid)
        else:
            raise ValueError(f"Unknown CNF strategy: {strategy_name}")

    def set_solver_algorithm(self, solver_name):
        """Thay đổi thuật toán giải CNF"""
        self.solver_algorithm = solver_name
        if solver_name not in [self.BRUTE_FORCE, self.BACKTRACKING, self.PYSAT]:
            raise ValueError(f"Unknown solver algorithm: {solver_name}")

    def solve(self):
        """Giải bài toán Thợ săn đá quý"""
        # Bắt đầu đo thời gian
        start_time = time.time()

        # Tạo CNF bằng chiến lược đã chọn
        cnf_clauses = self.cnf_strategy.generate_cnf()
        generation_time = time.time() - start_time

        print(f"Generated {len(cnf_clauses)} CNF clauses in {generation_time:.6f} seconds")
        clone_grid = self.grid.clone()
        # Chọn thuật toán giải CNF
        if self.solver_algorithm == self.BRUTE_FORCE:
            solver = BruteForceSolver(cnf_clauses, self.rows, self.cols, clone_grid)
        elif self.solver_algorithm == self.BACKTRACKING:
            solver = BacktrackingSolver(cnf_clauses, self.rows, self.cols, clone_grid)
        elif self.solver_algorithm == self.PYSAT:
            solver = PySATSolver(cnf_clauses, self.rows, self.cols, clone_grid)
        else:
            raise ValueError(f"Unknown solver algorithm: {self.solver_algorithm}")

        # Giải CNF
        solving_start_time = time.time()
        success, result_grid, solver_stats = solver.solve()
        solving_time = time.time() - solving_start_time

        total_time = time.time() - start_time

        # Trả về kết quả
        stats = {
            "success": success,
            "clauses": len(cnf_clauses),
            "cnf_strategy": self.cnf_strategy.__class__.__name__,
            "solver_algorithm": self.solver_algorithm,
            "generation_time": generation_time,
            "solving_time": solving_time,
            "total_time": total_time,
            "result_grid": result_grid
        }

        # Thêm thông tin từ solver
        if solver_stats:
            stats.update(solver_stats)

        return stats