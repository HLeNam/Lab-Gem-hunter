import os
import time
import matplotlib.pyplot as plt

from GemHunterGrid import GemHunterGrid
from GemHunterSolver import GemHunterSolver


def ensure_dir(directory):
    """Đảm bảo thư mục tồn tại"""
    if not os.path.exists(directory):
        os.makedirs(directory)


def solve_with_all_strategies(input_file, output_dir, max_time=300):
    """Giải bài toán với tất cả các chiến lược và thuật toán"""
    # Đọc lưới từ file
    grid = GemHunterGrid().load_grid_from_file(input_file)
    print(f"Loaded grid from {input_file}: {grid.rows}x{grid.cols}")

    # Tạo thư mục đầu ra nếu chưa tồn tại
    ensure_dir(output_dir)

    results = []

    # Các chiến lược CNF
    cnf_strategies = [
        GemHunterSolver.TRUTH_TABLE,
        GemHunterSolver.CARDINALITY
    ]

    # Các thuật toán giải
    solvers = [
        GemHunterSolver.BRUTE_FORCE,
        GemHunterSolver.BACKTRACKING,
        GemHunterSolver.PYSAT
    ]

    # Thử tất cả các kết hợp
    for cnf_strategy in cnf_strategies:
        for solver_algorithm in solvers:
            print(f"\n=== Testing {cnf_strategy} CNF with {solver_algorithm} solver ===\n")

            # Tạo bộ giải
            solver = GemHunterSolver(grid, cnf_strategy, solver_algorithm)

            # Thiết lập timeout
            start_time = time.time()
            success = False
            stats = None

            try:
                # Giải bài toán
                stats = solver.solve()
                success = stats["success"]

                # Lưu kết quả nếu thành công
                if success:
                    result_grid = GemHunterGrid(grid=stats["result_grid"])
                    output_file = os.path.join(output_dir,
                                               f"{cnf_strategy}_{solver_algorithm}_{os.path.basename(input_file).replace('input', 'output')}")
                    result_grid.save_grid_to_file(output_file)
                    print(f"Solution saved to {output_file}")
            except KeyboardInterrupt:
                print(f"Interrupted by user")
                stats = {
                    "success": False,
                    "interrupted": True,
                    "cnf_strategy": cnf_strategy,
                    "solver_algorithm": solver_algorithm,
                    "total_time": time.time() - start_time
                }
            except Exception as e:
                print(f"Error: {e}")
                stats = {
                    "success": False,
                    "error": str(e),
                    "cnf_strategy": cnf_strategy,
                    "solver_algorithm": solver_algorithm,
                    "total_time": time.time() - start_time
                }

            # Kiểm tra timeout
            if time.time() - start_time > max_time:
                print(f"Timeout after {max_time} seconds")
                stats = {
                    "success": False,
                    "timeout": True,
                    "cnf_strategy": cnf_strategy,
                    "solver_algorithm": solver_algorithm,
                    "total_time": max_time
                }

            # Thêm vào kết quả
            if stats:
                results.append(stats)

    return results


def create_comparison_plots(results, output_dir, test_case):
    """Tạo biểu đồ so sánh từ kết quả"""
    ensure_dir(output_dir)

    # Nhóm kết quả theo CNF strategy và solver algorithm
    grouped_results = {}
    for result in results:
        key = (result["cnf_strategy"], result["solver_algorithm"])
        grouped_results[key] = result

    # Tạo biểu đồ thời gian tạo CNF
    cnf_strategies = sorted(set(r["cnf_strategy"] for r in results))
    solvers = sorted(set(r["solver_algorithm"] for r in results))

    # Dữ liệu cho biểu đồ
    generation_times = []
    solving_times = []
    total_times = []
    labels = []

    for cnf in cnf_strategies:
        for solver in solvers:
            key = (cnf, solver)
            if key in grouped_results:
                result = grouped_results[key]
                generation_times.append(result.get("generation_time", 0))
                solving_times.append(result.get("solving_time", 0))
                total_times.append(result.get("total_time", 0))
                labels.append(f"{cnf}\n{solver}")
            else:
                generation_times.append(0)
                solving_times.append(0)
                total_times.append(0)
                labels.append(f"{cnf}\n{solver}")

    # Tạo biểu đồ thời gian
    plt.figure(figsize=(12, 8))
    width = 0.30
    x = range(len(labels))

    plt.bar([i - width for i in x], generation_times, width, label='Generation Time')
    plt.bar([i for i in x], solving_times, width, label='Solving Time')
    plt.bar([i + width for i in x], total_times, width, label='Total Time')

    plt.xlabel('CNF Strategy & Solver')
    plt.ylabel('Time (seconds)')
    plt.title(f'Performance Comparison - {os.path.basename(test_case)}')
    plt.xticks(x, labels)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Lưu biểu đồ
    plt.tight_layout()
    plot_file = os.path.join(output_dir, f"time_comparison_{os.path.basename(test_case).replace('.txt', '')}.png")
    plt.savefig(plot_file)
    plt.close()

    # Tạo biểu đồ số lượng clauses
    plt.figure(figsize=(8, 6))

    clauses = []
    cnf_labels = []

    for cnf in cnf_strategies:
        # Lấy số lượng clauses từ bất kỳ solver nào (vì chúng giống nhau cho cùng một CNF strategy)
        for solver in solvers:
            key = (cnf, solver)
            if key in grouped_results:
                result = grouped_results[key]
                clauses.append(result.get("clauses", 0))
                cnf_labels.append(cnf)
                break

    plt.bar(cnf_labels, clauses, color=['blue', 'green'])
    plt.xlabel('CNF Strategy')
    plt.ylabel('Number of Clauses')
    plt.title(f'Number of Clauses - {os.path.basename(test_case)}')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Lưu biểu đồ
    plt.tight_layout()
    plot_file = os.path.join(output_dir, f"clauses_comparison_{os.path.basename(test_case).replace('.txt', '')}.png")
    plt.savefig(plot_file)
    plt.close()

    # Tạo bảng so sánh
    with open(os.path.join(output_dir, f"comparison_{os.path.basename(test_case).replace('.txt', '')}.txt"), 'w') as f:
        f.write(f"Performance Comparison - {os.path.basename(test_case)}\n")
        f.write("=" * 50 + "\n\n")

        f.write(
            f"{'Strategy':<20} {'Solver':<15} {'Success':<8} {'Clauses':<10} {'Gen Time':<10} {'Solve Time':<12} {'Total Time':<12}\n")
        f.write("-" * 80 + "\n")

        for cnf in cnf_strategies:
            for solver in solvers:
                key = (cnf, solver)
                if key in grouped_results:
                    result = grouped_results[key]
                    f.write(
                        f"{cnf:<20} {solver:<15} {str(result['success']):<8} {result.get('clauses', 'N/A'):<10} {result.get('generation_time', 'N/A'):<10.4f} {result.get('solving_time', 'N/A'):<12.4f} {result.get('total_time', 'N/A'):<12.4f}\n")
                else:
                    f.write(f"{cnf:<20} {solver:<15} {'N/A':<8} {'N/A':<10} {'N/A':<10} {'N/A':<12} {'N/A':<12}\n")
            f.write("-" * 80 + "\n")


def main():
    # Tạo thư mục testcases, results và comparisons nếu chưa tồn tại
    ensure_dir("testcases")
    ensure_dir("results")
    ensure_dir("comparisons")

    # Tạo test case đơn giản nếu chưa có
    if not os.path.exists("testcases/input_simple.txt"):
        with open("testcases/input_simple.txt", "w") as f:
            f.write("1, _, _\n_, 2, _\n_, _, 1")

    # Kiểm tra và tạo test case nhỏ khác nếu chưa có
    if not os.path.exists("testcases/input_2x2.txt"):
        with open("testcases/input_2x2.txt", "w") as f:
            f.write("1, _\n_, 1")

    # Chạy so sánh cho từng test case
    test_cases = [
        "testcases/input_1.txt",
        "testcases/input_5x5.txt",
        "testcases/input_11x11.txt",
        "testcases/input_20x20.txt",
    ]

    for test_case in test_cases:
        if os.path.exists(test_case):
            print(f"\n=== Comparing all strategies for {test_case} ===\n")

            # Thiết lập timeout lâu hơn cho các bài toán lớn
            max_time = 600  # 10 phút

            results = solve_with_all_strategies(test_case, "results", max_time)
            create_comparison_plots(results, "comparisons", test_case)
        else:
            print(f"Warning: Test case {test_case} not found. Skipping...")


if __name__ == "__main__":
    main()