import time
from pysat.solvers import Solver

from ICNFSolver import ICNFSolver


class PySATSolver(ICNFSolver):
    """Giải CNF bằng thư viện PySAT"""

    def solve(self):
        """Giải CNF và trả về kết quả"""
        start_time = time.time()

        print(f"[PySAT] Solving with {len(self.clauses)} clauses...")

        with Solver(name='g4') as solver:
            # Thêm tất cả các mệnh đề vào bộ giải
            for clause in self.clauses:
                solver.add_clause(clause)

            # Kiểm tra xem có giải pháp không
            if solver.solve():
                # Lấy mô hình (các giá trị cho các biến)
                model = solver.get_model()

                solving_time = time.time() - start_time
                print(f"[PySAT] Found a solution")
                print(f"[PySAT] Solving time: {solving_time:.6f} seconds")

                # Tạo lưới kết quả
                result_grid = self.create_result_grid(model)

                return True, result_grid, {
                    "solving_time": solving_time
                }
            else:
                solving_time = time.time() - start_time
                print(f"[PySAT] No solution found")
                print(f"[PySAT] Solving time: {solving_time:.6f} seconds")

                return False, None, {
                    "solving_time": solving_time
                }