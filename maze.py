class Cell:
    def __init__(self, y=None, x=None):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.y} e {self.x}"
    
    def __eq__(self, other):
            return self.x == other.x and self.y == other.y
            

class Maze:
    def __init__(self, maze_data):
        self.matrix_maze = maze_data

        self.cheese_marker = 'e'
        self.mouse_marker = 'm'
        self.visited_marker = '.'
        self.passage_marker = '0'
        self.wall_marker = '1'

        self.maze_stack = []  # correct path mouse to cheese

        self.width = len(maze_data[0])
        self.height = len(maze_data)

        self.mouse_cell = self.find_cell(self.mouse_marker)
        self.current_cell = self.mouse_cell
        self.cheese_cell = self.find_cell(self.cheese_marker)

    def find_cell(self, marker):
        for y in range(self.height):
            for x in range(self.width):
                if self.matrix_maze[y][x] == marker:
                    return Cell(y, x)


    