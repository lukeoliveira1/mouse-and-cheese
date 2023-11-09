import pygame

from maze import Cell, Maze
from variables import variables
from load_txt import load_txt_maze

mouse_image = pygame.image.load("imgs/mouse.gif")
cheese_image = pygame.image.load("imgs/cheese.gif")

mouse_image = pygame.transform.scale(
    mouse_image, (variables["SCREEN_SIZE"], variables["SCREEN_SIZE"])
)
cheese_image = pygame.transform.scale(
    cheese_image, (variables["SCREEN_SIZE"], variables["SCREEN_SIZE"])
)

pygame.init()

maze = Maze(load_txt_maze("txts/maze5.txt"))

screen = pygame.display.set_mode(
    (maze.width * variables["SCREEN_SIZE"], maze.height * variables["SCREEN_SIZE"])
)

pygame.display.set_caption("Mouse&Cheese Maze")


def mark_visited(cell):
    maze.matrix_maze[cell.y][cell.x] = maze.visited_marker


running = True
found_cheese = False

while running:

    screen.fill(variables["RED"])

    for y in range(maze.height):  # rows
        for x in range(maze.width):  # columns

            square = pygame.Rect(
                x * variables["SCREEN_SIZE"],
                y * variables["SCREEN_SIZE"],
                variables["SCREEN_SIZE"],
                variables["SCREEN_SIZE"],
            )

            if maze.matrix_maze[y][x] == maze.wall_marker:
                pygame.draw.rect(screen, variables["GRAY"], square)

            elif maze.matrix_maze[y][x] == maze.passage_marker:
                pygame.draw.rect(screen, variables["WHITE"], square)

            elif maze.matrix_maze[y][x] == '_':
                pygame.draw.rect(screen, variables["GREEN"], square)

    if not found_cheese:
        if maze.current_cell == maze.cheese_cell:
            found_cheese = True
            print("Achou o queijo!")
            print("Veja seu caminho:")

            while maze.maze_stack:
                cell = maze.maze_stack.pop()
                print("Coordenadas do rato até o queijo: ", cell.y, cell.x)
                maze.matrix_maze[cell.y][cell.x] = '_'
                
        else:
            mark_visited(maze.current_cell)

            neighbors = []
            for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ny, nx = maze.current_cell.y + dy, maze.current_cell.x + dx
                if (
                    0 <= ny < maze.height
                    and 0 <= nx < maze.width
                    and maze.matrix_maze[ny][nx] != maze.wall_marker
                    and maze.matrix_maze[ny][nx] != maze.visited_marker
                ):
                    neighbors.append(Cell(ny, nx))

            if neighbors:
                maze.maze_stack.append(maze.current_cell)

                next_cell = neighbors[0]

                maze.maze_stack.append(next_cell)

                # for cell in maze.maze_stack:
                #     print("cells vizinhas:", cell.y, cell.x)

                pygame.time.delay(10)

                maze.current_cell = next_cell

                # print(
                #     "posição visitada: ",
                #     maze.matrix_maze[maze.current_cell.y][maze.current_cell.x],
                #     "coordenadas: ",
                #     maze.current_cell.y,
                #     maze.current_cell.x,
                # )

            else:
                if not maze.maze_stack:
                    print("Caminho não encontrado, rato preso")
                    break
                else:
                    maze.current_cell = maze.maze_stack.pop()

    screen.blit(
        mouse_image,
        (
            maze.current_cell.x * variables["SCREEN_SIZE"],
            maze.current_cell.y * variables["SCREEN_SIZE"],
        ),
    )

    screen.blit(
        cheese_image,
        (
            maze.cheese_cell.x * variables["SCREEN_SIZE"],
            maze.cheese_cell.y * variables["SCREEN_SIZE"],
        ),
    )

    pygame.display.update()