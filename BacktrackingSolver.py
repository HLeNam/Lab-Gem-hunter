import time

from ICNFSolver import ICNFSolver


class BacktrackingSolver(ICNFSolver):
    def solve(self):
        start_time = time.time()

        var_list = set()
        for clause in self.clauses:
            for var in clause:
                var_list.add(abs(var))

        var_list = sorted(list(var_list))
        num_vars = len(var_list)

        # Thống kê số lần xuất hiện của mỗi biến để ưu tiên
        var_count = {var: 0 for var in var_list}
        for clause in self.clauses:
            for var in clause:
                var_count[abs(var)] += 1

        # Sắp xếp lại biến theo số lần xuất hiện (giảm dần)
        var_list.sort(key=lambda var: var_count[var], reverse=True)

        print(f"[Backtracking] Solving with {num_vars} variables and {len(self.clauses)} clauses...")

        # Trạng thái backtracking
        stats = {
            "decisions": 0,
            "backtracks": 0
        }

        # Mô hình hiện tại (assignment)
        assignment = {}

        # Kiểm tra xem một mệnh đề có thỏa mãn không với gán giá trị hiện tại
        def is_clause_satisfied(clause):
            for var in clause:
                var_abs = abs(var)
                if var_abs in assignment:
                    if (var > 0 and assignment[var_abs]) or (var < 0 and not assignment[var_abs]):
                        return True
            return False

        # Kiểm tra xem một mệnh đề có thể trở thành đơn vị không (unit clause)
        def is_unit_clause(clause):
            unassigned = []
            for var in clause:
                var_abs = abs(var)
                if var_abs not in assignment:
                    unassigned.append(var)
                elif (var > 0 and assignment[var_abs]) or (var < 0 and not assignment[var_abs]):
                    return None  # Mệnh đề đã thỏa mãn

            if len(unassigned) == 1:
                return unassigned[0]  # Trả về biến đơn vị
            return None

        # Kiểm tra xem một mệnh đề có thể trở thành xung đột không (conflicting clause)
        def is_conflicting_clause(clause):
            for var in clause:
                var_abs = abs(var)
                if var_abs not in assignment:
                    return False  # Vẫn còn biến chưa gán
                if (var > 0 and assignment[var_abs]) or (var < 0 and not assignment[var_abs]):
                    return False  # Mệnh đề đã thỏa mãn
            return True  # Tất cả biến đã gán và không có biến nào thỏa mãn mệnh đề

        # Tìm kiếm unit propagation
        def unit_propagation():
            while True:
                unit_var = None
                for clause in self.clauses:
                    if is_clause_satisfied(clause):
                        continue
                    unit = is_unit_clause(clause)
                    if unit is not None:
                        unit_var = unit
                        break

                if unit_var is None:
                    break

                # Gán giá trị cho biến đơn vị
                var_abs = abs(unit_var)
                assignment[var_abs] = (unit_var > 0)

            # Kiểm tra xem có mệnh đề nào xung đột không
            for clause in self.clauses:
                if is_conflicting_clause(clause):
                    return False
            return True

        def backtrack(index):
            # Kiểm tra tiến độ
            stats["decisions"] += 1
            if stats["decisions"] % 1000 == 0:
                elapsed = time.time() - start_time
                print(
                    f"[Backtracking] Decisions: {stats['decisions']:,}, Backtracks: {stats['backtracks']:,} - {elapsed:.2f} seconds elapsed")

            # Nếu đã gán giá trị cho tất cả các biến và thỏa mãn tất cả các mệnh đề
            if index == len(var_list):
                return True

            # Chọn biến tiếp theo
            var = var_list[index]

            # Thử các giá trị có thể (True và False)
            for value in [True, False]:
                # Gán giá trị cho biến
                old_assignment = assignment.copy()
                assignment[var] = value

                # Thực hiện unit propagation
                if unit_propagation():
                    # Nếu không có mâu thuẫn, tiếp tục với biến tiếp theo
                    if backtrack(index + 1):
                        return True

                # Quay lui
                stats["backtracks"] += 1

                # Khôi phục trạng thái trước khi gán giá trị
                assignment.clear()
                assignment.update(old_assignment)

            return False

        success = False
        try:
            # Thực hiện unit propagation ban đầu
            if unit_propagation():
                # Ghi nhớ các biến đã gán trước khi backtracking
                assigned_before = set(assignment.keys())
                # Bắt đầu backtracking
                success = backtrack(0)
        except KeyboardInterrupt:
            print("[Backtracking] Interrupted by user")

        solving_time = time.time() - start_time

        if success:
            print(
                f"[Backtracking] Found a solution after {stats['decisions']:,} decisions and {stats['backtracks']:,} backtracks")
            print(f"[Backtracking] Solving time: {solving_time:.6f} seconds")

            # Tạo mô hình từ gán giá trị
            model = []
            for var in var_list:
                if var in assignment:
                    if assignment[var]:
                        model.append(var)
                    else:
                        model.append(-var)

            # Tạo lưới kết quả
            result_grid = self.create_result_grid(model)

            return True, result_grid, {
                "decisions": stats["decisions"],
                "backtracks": stats["backtracks"],
                "solving_time": solving_time
            }
        else:
            print(
                f"[Backtracking] No solution found after {stats['decisions']:,} decisions and {stats['backtracks']:,} backtracks")
            print(f"[Backtracking] Solving time: {solving_time:.6f} seconds")

            return False, None, {
                "decisions": stats["decisions"],
                "backtracks": stats["backtracks"],
                "solving_time": solving_time
            }