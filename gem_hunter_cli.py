import argparse
import os

from GemHunterGrid import GemHunterGrid
from GemHunterSolver import GemHunterSolver


def main():
    parser = argparse.ArgumentParser(description='Giải bài toán Thợ săn đá quý.')
    parser.add_argument('input', help='Đường dẫn đến file đầu vào')
    parser.add_argument('-o', '--output', help='Đường dẫn đến file đầu ra')
    parser.add_argument('-s', '--strategy', choices=['truth_table', 'cardinality'],
                        default='cardinality', help='Chiến lược tạo CNF (mặc định: cardinality)')
    parser.add_argument('-v', '--verbose', action='store_true', help='In thông tin chi tiết')

    args = parser.parse_args()

    # Tạo đường dẫn đầu ra nếu không được chỉ định
    if not args.output:
        output_dir = "results"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        args.output = os.path.join(output_dir,
                                   f"{args.strategy}_{os.path.basename(args.input).replace('input', 'output')}")

    # Đọc lưới từ file
    grid = GemHunterGrid().load_grid_from_file(args.input)

    if args.verbose:
        print(f"Loaded grid from {args.input}:")
        print(grid)

    # Giải bài toán
    solver = GemHunterSolver(grid, args.strategy)
    stats = solver.solve()

    if stats["success"]:
        # Lưu kết quả
        result_grid = GemHunterGrid(grid=stats["result_grid"])
        result_grid.save_grid_to_file(args.output)

        print(f"Found solution using {args.strategy} strategy:")
        print(f"- Number of clauses: {stats['clauses']}")
        print(f"- Time to generate CNF: {stats['generation_time']:.6f} seconds")
        print(f"- Time to solve: {stats['solving_time']:.6f} seconds")
        print(f"- Total time: {stats['total_time']:.6f} seconds")
        print(f"Solution saved to {args.output}")

        if args.verbose:
            print("\nSolution:")
            print(result_grid)
    else:
        print(f"Could not find a solution using {args.strategy} strategy.")
        print(f"- Number of clauses: {stats['clauses']}")
        print(f"- Time spent: {stats['total_time']:.6f} seconds")


if __name__ == "__main__":
    main()