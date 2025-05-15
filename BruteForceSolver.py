import time
from itertools import product

from ICNFSolver import ICNFSolver

class BruteForceSolver(ICNFSolver):
    def solve(self):
        start_time = time.time()

        var_list = set()
        for clause in self.clauses:
            for var in clause:
                var_list.add(abs(var))

        var_list = sorted(list(var_list))
        num_vars = len(var_list)

        print(f"[Brute Force] Solving with {num_vars} variables and {len(self.clauses)} clauses...")

        total_combinations = 2 ** num_vars
        checked = 0

        var_to_index = {var: i for i, var in enumerate(var_list)}

        for values in product([False, True], repeat=num_vars):
            # Kiểm tra tiến độ
            checked += 1
            if checked % 1000 == 0 or checked == total_combinations:
                progress = (checked / total_combinations) * 100
                elapsed = time.time() - start_time
                print(
                    f"[Brute Force] Checked {checked:,}/{total_combinations:,} combinations ({progress:.2f}%) - {elapsed:.2f} seconds elapsed")

            model = []
            for i, value in enumerate(values):
                if value:
                    model.append(var_list[i])
                else:
                    model.append(-var_list[i])

            satisfied = True
            for clause in self.clauses:
                clause_satisfied = False
                for var in clause:
                    var_index = var_to_index[abs(var)]
                    var_value = values[var_index]

                    # Nếu biến là dương và giá trị True, hoặc biến là âm và giá trị False
                    if (var > 0 and var_value) or (var < 0 and not var_value):
                        clause_satisfied = True
                        break

                if not clause_satisfied:
                    satisfied = False
                    break

            if satisfied:
                solving_time = time.time() - start_time
                print(f"[Brute Force] Found a solution after checking {checked:,}/{total_combinations:,} combinations")
                print(f"[Brute Force] Solving time: {solving_time:.6f} seconds")

                # Tạo lưới kết quả
                result_grid = self.create_result_grid(model)

                return True, result_grid, {
                    "checked_combinations": checked,
                    "total_combinations": total_combinations,
                    "solving_time": solving_time
                }

        # Nếu không tìm thấy nghiệm nào
        solving_time = time.time() - start_time
        print(f"[Brute Force] No solution found after checking all {total_combinations:,} combinations")
        print(f"[Brute Force] Solving time: {solving_time:.6f} seconds")

        return False, None, {
            "checked_combinations": checked,
            "total_combinations": total_combinations,
            "solving_time": solving_time
        }