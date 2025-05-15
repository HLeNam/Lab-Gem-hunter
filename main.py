import GemHunterGrid

if __name__ == "__main__":
    # Create a grid with 5 rows and 5 columns
    grid = GemHunterGrid.GemHunterGrid()

    # Load the grid from a file
    grid.load_grid_from_file("./testcases/input_1.txt")

    # Print the grid
    print(grid)

    # Save the grid to a file
    grid.save_grid_to_file("output.txt")

    # Get neighbors of a specific cell
    neighbors = grid.get_neighbors(2, 2)
    print("Neighbors of (2, 2):", neighbors)