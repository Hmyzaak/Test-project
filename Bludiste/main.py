import random
from typing import List, Tuple


class Maze:
    # Typy políček
    WALL = "#"
    EMPTY = "."
    BASE = "X"

    def __init__(self, rows: int = 11, cols: int = 11):
        self.rows = rows
        self.cols = cols
        self.grid = [[self.EMPTY for _ in range(cols)] for _ in range(rows)]
        self._initialize_maze()

    def _initialize_maze(self):
        # Vytvoření zdí na obvodu
        for r in range(self.rows):
            for c in range(self.cols):
                if r == 0 or r == self.rows - 1 or c == 0 or c == self.cols - 1:
                    self.grid[r][c] = self.WALL

        # Přidání základových polí
        base_positions = [
            (2, 2), (2, 4), (2, 6), (2, 8),
            (4, 2), (4, 4), (4, 6), (4, 8),
            (6, 2), (6, 4), (6, 6), (6, 8),
            (8, 2), (8, 4), (8, 6), (8, 8),
        ]
        for r, c in base_positions:
            self.grid[r][c] = self.BASE

    def count_bases(self) -> int:
        """Spočítá zbývající základová políčka."""
        return sum(row.count(self.BASE) for row in self.grid)

    def display(self):
        """Vykreslí bludiště do konzole."""
        for row in self.grid:
            print(" ".join(row))

    def random_base(self) -> Tuple[int, int]:
        """Vybere náhodné základové políčko."""
        bases = [(r, c) for r in range(self.rows) for c in range(self.cols) if self.grid[r][c] == self.BASE]
        return random.choice(bases)


# Hlavní část programu
if __name__ == "__main__":
    maze = Maze()
    maze.display()
    print(f"Zbývající základová políčka: {maze.count_bases()}")
    random_base = maze.random_base()
    print(f"Náhodně vybrané základové políčko: {random_base}")
