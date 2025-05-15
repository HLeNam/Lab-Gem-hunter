import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt

from GemHunterGrid import GemHunterGrid
from GemHunterSolver import GemHunterSolver


def ensure_dir(directory):
    """Đảm bảo thư mục tồn tại"""
    if not os.path.exists(directory):
        os.makedirs(directory)


def run_benchmark(input_file, strategies, repeat=3):
    """Chạy benchmark cho một file đầu vào với các chiến lược khác nhau"""
    grid = GemHunterGrid().load_grid_from_file(input_file)
    results = []

    for strategy in strategies:
        print(f"Testing {input_file} with {strategy} strategy...")

        # Chạy nhiều lần để lấy kết quả trung bình
        strategy_results = []
        for run in range(repeat):
            solver = GemHunterSolver(grid, strategy)
            stats = solver.solve()
            strategy_results.append(stats)

        # Tính trung bình các giá trị
        avg_clauses = sum(r["clauses"] for r in strategy_results) / repeat
        avg_generation_time = sum(r["generation_time"] for r in strategy_results) / repeat
        avg_solving_time = sum(r["solving_time"] for r in strategy_results) / repeat
        avg_total_time = sum(r["total_time"] for r in strategy_results) / repeat

        results.append({
            "input": os.path.basename(input_file),
            "strategy": strategy,
            "grid_size": f"{grid.rows}x{grid.cols}",
            "clauses": int(avg_clauses),
            "generation_time": avg_generation_time,
            "solving_time": avg_solving_time,
            "total_time": avg_total_time
        })

    return results


def create_report(benchmark_results, output_dir):
    """Tạo báo cáo từ kết quả benchmark"""
    ensure_dir(output_dir)

    # Tạo DataFrame từ kết quả
    df = pd.DataFrame(benchmark_results)

    # Lưu file CSV
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = os.path.join(output_dir, f"benchmark_results_{timestamp}.csv")
    df.to_csv(csv_file, index=False)
    print(f"Benchmark results saved to {csv_file}")

    # Tạo báo cáo tóm tắt
    summary_file = os.path.join(output_dir, f"benchmark_summary_{timestamp}.txt")
    with open(summary_file, "w") as f:
        f.write("Benchmark Summary\n")
        f.write("=================\n\n")

        # Nhóm theo kích thước lưới và chiến lược
        grouped = df.groupby(["grid_size", "strategy"])

        for (grid_size, strategy), group in grouped:
            f.write(f"Grid Size: {grid_size}, Strategy: {strategy}\n")
            f.write(f"- Average clauses: {group['clauses'].mean():.0f}\n")
            f.write(f"- Average generation time: {group['generation_time'].mean():.6f} seconds\n")
            f.write(f"- Average solving time: {group['solving_time'].mean():.6f} seconds\n")
            f.write(f"- Average total time: {group['total_time'].mean():.6f} seconds\n\n")

    print(f"Benchmark summary saved to {summary_file}")

    # Tạo biểu đồ
    create_benchmark_plots(df, output_dir, timestamp)


def create_benchmark_plots(df, output_dir, timestamp):
    """Tạo các biểu đồ từ kết quả benchmark"""
    # Biểu đồ số lượng mệnh đề
    plt.figure(figsize=(10, 6))

    # Nhóm theo kích thước lưới và chiến lược
    pivot_clauses = df.pivot_table(values="clauses", index="grid_size", columns="strategy")

    # Vẽ biểu đồ
    ax = pivot_clauses.plot(kind="bar", color=["blue", "green"])
    plt.title("Số lượng mệnh đề CNF theo kích thước lưới")
    plt.ylabel("Số mệnh đề")
    plt.xlabel("Kích thước lưới")
    plt.legend(title="Chiến lược")
    plt.tight_layout()

    # Lưu biểu đồ
    clauses_plot_file = os.path.join(output_dir, f"clauses_comparison_{timestamp}.png")
    plt.savefig(clauses_plot_file)
    plt.close()

    # Biểu đồ thời gian tạo CNF
    plt.figure(figsize=(10, 6))
    pivot_generation = df.pivot_table(values="generation_time", index="grid_size", columns="strategy")
    ax = pivot_generation.plot(kind="bar", color=["blue", "green"])
    plt.title("Thời gian tạo CNF theo kích thước lưới")
    plt.ylabel("Thời gian (giây)")
    plt.xlabel("Kích thước lưới")
    plt.legend(title="Chiến lược")
    plt.tight_layout()
    generation_plot_file = os.path.join(output_dir, f"generation_time_comparison_{timestamp}.png")
    plt.savefig(generation_plot_file)
    plt.close()

    # Biểu đồ thời gian giải
    plt.figure(figsize=(10, 6))
    pivot_solving = df.pivot_table(values="solving_time", index="grid_size", columns="strategy")
    ax = pivot_solving.plot(kind="bar", color=["blue", "green"])
    plt.title("Thời gian giải CNF theo kích thước lưới")
    plt.ylabel("Thời gian (giây)")
    plt.xlabel("Kích thước lưới")
    plt.legend(title="Chiến lược")
    plt.tight_layout()
    solving_plot_file = os.path.join(output_dir, f"solving_time_comparison_{timestamp}.png")
    plt.savefig(solving_plot_file)
    plt.close()

    # Biểu đồ tổng thời gian
    plt.figure(figsize=(10, 6))
    pivot_total = df.pivot_table(values="total_time", index="grid_size", columns="strategy")
    ax = pivot_total.plot(kind="bar", color=["blue", "green"])
    plt.title("Tổng thời gian theo kích thước lưới")
    plt.ylabel("Thời gian (giây)")
    plt.xlabel("Kích thước lưới")
    plt.legend(title="Chiến lược")
    plt.tight_layout()
    total_plot_file = os.path.join(output_dir, f"total_time_comparison_{timestamp}.png")
    plt.savefig(total_plot_file)
    plt.close()

    print(f"Benchmark plots saved to {output_dir}")


def main():
    # Tạo thư mục testcases và benchmark nếu chưa tồn tại
    ensure_dir("testcases")
    ensure_dir("benchmark")

    # Kiểm tra xem test cases đã tồn tại chưa
    test_cases = [
        "testcases/input_simple.txt",  # 3x3
        "testcases/input_1.txt",  # 3x4
        "testcases/input_5x5.txt",  # 5x5
        "testcases/input_11x11.txt"  # 11x11
    ]

    # Các chiến lược cần benchmark
    strategies = [GemHunterSolver.TRUTH_TABLE, GemHunterSolver.CARDINALITY]

    # Chạy benchmark
    all_results = []
    for test_case in test_cases:
        if os.path.exists(test_case):
            results = run_benchmark(test_case, strategies)
            all_results.extend(results)
        else:
            print(f"Warning: Test case {test_case} not found. Skipping...")

    # Tạo báo cáo
    create_report(all_results, "benchmark")


if __name__ == "__main__":
    main()