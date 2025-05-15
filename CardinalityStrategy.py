from itertools import combinations

from CNFGenerator import CNFGenerator


class CardinalityStrategy(CNFGenerator):

    def generate_at_least_n_clauses(self, neighbors, n):
        """Tạo mệnh đề 'ít nhất n bẫy' từ các ô lân cận"""
        if n == 0:
            return []  # Không cần ràng buộc nếu n=0

        clauses = []
        k = len(neighbors)

        # Nếu cần tất cả các ô là bẫy
        if n == k:
            for i, j in neighbors:
                clauses.append([self.position_to_variable(i, j)])
            return clauses

        # Công thức: nếu có ít nhất n bẫy trong k ô,
        # thì không thể có (k-n+1) ô không phải bẫy
        # Ta tạo mệnh đề cho tất cả các tổ hợp (k-n+1) ô
        for combo in combinations(neighbors, k - n + 1):
            # Mệnh đề: "Ít nhất một trong những ô này phải là bẫy"
            clause = [self.position_to_variable(i, j) for i, j in combo]
            clauses.append(clause)

        return clauses

    def generate_at_most_n_clauses(self, neighbors, n):
        """Tạo mệnh đề 'nhiều nhất n bẫy' từ các ô lân cận"""
        if n >= len(neighbors):
            return []  # Không cần ràng buộc nếu n ≥ số lượng hàng xóm

        clauses = []

        # Nếu không được có bẫy nào
        if n == 0:
            for i, j in neighbors:
                clauses.append([-self.position_to_variable(i, j)])
            return clauses

        # Công thức: nếu có nhiều nhất n bẫy trong k ô,
        # thì không thể có (n+1) ô đều là bẫy
        # Ta tạo mệnh đề cho tất cả các tổ hợp (n+1) ô
        for combo in combinations(neighbors, n + 1):
            # Mệnh đề: "Ít nhất một trong những ô này không phải là bẫy"
            clause = [-self.position_to_variable(i, j) for i, j in combo]
            clauses.append(clause)

        return clauses

    def generate_exactly_n_clauses(self, neighbors, n):
        """Tạo mệnh đề 'chính xác n bẫy' bằng cách kết hợp 'ít nhất n' và 'nhiều nhất n'"""
        at_least_clauses = self.generate_at_least_n_clauses(neighbors, n)
        at_most_clauses = self.generate_at_most_n_clauses(neighbors, n)
        return at_least_clauses + at_most_clauses
