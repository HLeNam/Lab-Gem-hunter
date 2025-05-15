import os
import time
import matplotlib.pyplot as plt

from GemHunterGrid import GemHunterGrid
from GemHunterSolver import GemHunterSolver


def ensure_dir(directory):
    """Đảm bảo thư mục tồn tại"""
    if not os.path.exists(directory):
        os.makedirs(directory)


def solve_with_strategy(input_file, output_dir, strategy_name):
    """Giải bài toán Thợ săn đá quý với một chiến lược cụ thể"""
    # Đọc lưới từ file
    grid = GemHunterGrid().load_grid_from_file(input_file)
    print(f"[{strategy_name.upper()}] Loaded grid from {input_file}")

    # Tạo thư mục đầu ra nếu chưa tồn tại
    ensure_dir(output_dir)

    # Tạo bộ giải và giải bài toán
    solver = GemHunterSolver(grid, strategy_name)
    stats = solver.solve()

    if stats["success"]:
        result_grid = GemHunterGrid(grid=stats["result_grid"])
        output_file = os.path.join(output_dir,
                                   f"{strategy_name}_{os.path.basename(input_file).replace('input', 'output')}")
        result_grid.save_grid_to_file(output_file)
        print(f"[{strategy_name.upper()}] Solution saved to {output_file}")
        print(
            f"[{strategy_name.upper()}] Generated {stats['clauses']} clauses in {stats['generation_time']:.6f} seconds")
        print(f"[{strategy_name.upper()}] Solved in {stats['solving_time']:.6f} seconds")
        print(f"[{strategy_name.upper()}] Total time: {stats['total_time']:.6f} seconds")
    else:
        print(f"[{strategy_name.upper()}] Could not find a solution. Time spent: {stats['total_time']:.6f} seconds")

    return stats


def create_comparison_plot(test_case, tt_stats, card_stats, plot_dir):
    """Tạo biểu đồ so sánh giữa hai chiến lược"""
    ensure_dir(plot_dir)

    # Thiết lập biểu đồ
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Biểu đồ số lượng mệnh đề
    methods = ['Truth Table', 'Cardinality']
    num_clauses = [tt_stats['clauses'], card_stats['clauses']]

    ax1.bar(methods, num_clauses, color=['blue', 'green'])
    ax1.set_title('Số lượng mệnh đề CNF')
    ax1.set_ylabel('Số mệnh đề')
    for i, v in enumerate(num_clauses):
        ax1.text(i, v + 0.1, str(v), ha='center')

    # Biểu đồ thời gian
    width = 0.35
    x = range(len(methods))

    # Chuẩn bị dữ liệu thời gian
    generation_times = [tt_stats['generation_time'], card_stats['generation_time']]
    solving_times = [tt_stats['solving_time'], card_stats['solving_time']]

    ax2.bar([p - width / 2 for p in x], generation_times, width, label='Thời gian tạo CNF')
    ax2.bar([p + width / 2 for p in x], solving_times, width, label='Thời gian giải')
    ax2.set_title('Thời gian thực thi (giây)')
    ax2.set_xticks(x)
    ax2.set_xticklabels(methods)
    ax2.legend()

    for i, v in enumerate(generation_times):
        ax2.text(i - width / 2, v + 0.001, f"{v:.4f}", ha='center', fontsize=8)
    for i, v in enumerate(solving_times):
        ax2.text(i + width / 2, v + 0.001, f"{v:.4f}", ha='center', fontsize=8)

    plt.tight_layout()

    # Lưu biểu đồ
    plot_file = os.path.join(plot_dir, f"comparison_{os.path.basename(test_case).replace('.txt', '')}.png")
    plt.savefig(plot_file)
    print(f"Comparison plot saved to {plot_file}")
    plt.close()


def main():
    # Tạo thư mục testcases, results và plots nếu chưa tồn tại
    ensure_dir("testcases")
    ensure_dir("results")
    ensure_dir("plots")

    # Kiểm tra xem test cases đã tồn tại chưa, nếu chưa thì tạo
    test_cases = [
        "input_simple.txt",  # 3x3
        "input_1.txt",  # 3x4
        "input_5x5.txt",  # 5x5
        "input_11x11.txt"  # 11x11
    ]

    # Kiểm tra và tạo test case đơn giản nếu chưa có
    if not os.path.exists("testcases/input_simple.txt"):
        with open("testcases/input_simple.txt", "w") as f:
            f.write("1, _, _\n_, 2, _\n_, _, 1")

    # Kiểm tra và tạo test case 3x4 nếu chưa có
    if not os.path.exists("testcases/input_1.txt"):
        with open("testcases/input_1.txt", "w") as f:
            f.write("3, _, 2, _\n_, _, 2, _\n_, 3, 1, _")

    # Thử nghiệm với các test case
    for test_case in test_cases:
        test_path = os.path.join("testcases", test_case)
        if not os.path.exists(test_path):
            print(f"Warning: Test case {test_path} not found. Skipping...")
            continue

        print(f"\n=== Testing {test_case} ===\n")

        # Giải với cả hai chiến lược
        try:
            card_stats = solve_with_strategy(test_path, "results", GemHunterSolver.CARDINALITY)
            print("\n")
            tt_stats = solve_with_strategy(test_path, "results", GemHunterSolver.TRUTH_TABLE)

            # Tạo biểu đồ so sánh
            if card_stats["success"] and tt_stats["success"]:
                create_comparison_plot(test_case, tt_stats, card_stats, "plots")
        except Exception as e:
            print(f"Error when processing {test_case}: {e}")


if __name__ == "__main__":
    main()