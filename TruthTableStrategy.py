from CNFGenerator import CNFGenerator

class TruthTableStrategy(CNFGenerator):
    def generate_exactly_n_clauses(self, neighbors, n):
        """Tạo mệnh đề 'chính xác n bẫy' sử dụng phương pháp bảng sự thật"""
        # Trường hợp đặc biệt
        if n == 0:
            # Tất cả các ô đều không phải bẫy
            return [[-self.position_to_variable(i, j)] for i, j in neighbors]

        if n == len(neighbors):
            # Tất cả các ô đều là bẫy
            return [[self.position_to_variable(i, j)] for i, j in neighbors]

        clauses = []
        k = len(neighbors)

        # Tạo ra tất cả các khả năng có thể (2^k trường hợp)
        for bits in range(2 ** k):
            bit_string = format(bits, f'0{k}b')
            count_true = bit_string.count('1')

            # Nếu số lượng '1' khác n, tạo mệnh đề loại trừ trường hợp này
            if count_true != n:
                # Để phủ định một trường hợp cụ thể, chúng ta tạo một mệnh đề
                # mà mỗi bit được đảo ngược thành "ít nhất một biến phải khác giá trị này"
                clause = []

                for idx, bit in enumerate(bit_string):
                    i, j = neighbors[idx]
                    var = self.position_to_variable(i, j)

                    # Nếu bit = 1 (là bẫy) trong trường hợp này,
                    # phủ định là "vị trí này không phải bẫy"
                    if bit == '1':
                        clause.append(-var)
                    # Nếu bit = 0 (không phải bẫy), phủ định là "vị trí này là bẫy"
                    else:
                        clause.append(var)

                clauses.append(clause)

        return clauses