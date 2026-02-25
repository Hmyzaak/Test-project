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

    def get_valid_directions(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Vrací seznam směrů, kam lze stavět zeď."""
        directions = []
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Nahoru, dolů, doleva, doprava

        for dr, dc in moves:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.grid[nr][nc] in {self.EMPTY, self.BASE}:
                    directions.append((dr, dc))
        return directions

    def build_wall(self, start_row: int, start_col: int):
        """Generuje zeď od daného základového políčka."""
        current_row, current_col = start_row, start_col

        while True:
            directions = self.get_valid_directions(current_row, current_col)
            if not directions:
                break  # Pokud nejsou žádné volné směry, ukončíme

            # Náhodně vybereme směr a pokračujeme
            dr, dc = random.choice(directions)
            next_row, next_col = current_row + dr, current_col + dc

            self.grid[current_row][current_col] = self.WALL
            current_row, current_col = next_row, next_col

            # Pokud narazíme na zeď, ukončíme stavění
            if self.grid[current_row][current_col] == self.WALL:
                break
            else:
                self.grid[current_row][current_col] = self.WALL

    def generate_maze(self):
        """Hlavní smyčka pro generování zdí."""
        while self.count_bases() > 0:
            base_row, base_col = self.random_base()
            self.build_wall(base_row, base_col)


# Hlavní část programu
if __name__ == "__main__":
    maze = Maze()
    print("Bludiště před generováním zdí:")
    maze.display()

    maze.generate_maze()
    print("\nBludiště po generování zdí:")
    maze.display()
