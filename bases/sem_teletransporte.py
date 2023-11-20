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

maze = Maze(load_txt_maze("txts/maze2.txt"))

screen = pygame.display.set_mode(
    (maze.width * variables["SCREEN_SIZE"], maze.height * variables["SCREEN_SIZE"])
)

pygame.display.set_caption("Mouse&Cheese Maze")


def mark_visited(cell):
    maze.matrix_maze[cell.y][cell.x] = maze.visited_marker


running = True
found_cheese = False

while running:
    # screen.fill((255, 255, 255))
    screen.fill(variables["RED"])

    for y in range(maze.height):  # linhas
        for x in range(maze.width):  # colunas
            #    coordenada x   coordenada y    width        height
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

            elif maze.matrix_maze[y][x] == "_":
                pygame.draw.rect(screen, variables["GREEN"], square)

    if not found_cheese:
        if maze.current_cell == maze.cheese_cell:
            found_cheese = True
            print("Achou o queijo sabichão!")
            print("Veja seu caminho:")

            for cell in maze.maze_stack:
                print("Coordenadas do sucesso:", cell.y, cell.x)
                maze.matrix_maze[cell.y][cell.x] = "_"
            maze.matrix_maze[maze.cheese_cell.y][maze.cheese_cell.x] = "_"

        else:
            mark_visited(maze.current_cell)

            # Verifique os vizinhos não visitados
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
                # Adicione a célula atual à pilha
                maze.maze_stack.append(maze.current_cell)
                # Escolha um vizinho
                next_cell = neighbors[0]
                # Adicione o vizinho à pilha
                maze.maze_stack.append(next_cell)
                # Atualize a célula atual
                maze.current_cell = next_cell
            else:
                if not maze.maze_stack:
                    print("Caminho não encontrado, rato preso")
                    break
                else:
                    # Faça um pop na pilha e o faça como a célula atual
                    maze.current_cell = maze.maze_stack.pop()
                    print("Preso mas achou o caminho")

            if maze.maze_stack:
                next_cell = maze.maze_stack.pop()

                mark_visited(maze.current_cell)

                # for cell in maze.maze_stack:
                #     print("NEIGHBOORS:", cell.y, cell.x)

                pygame.time.delay(100)

                maze.current_cell = next_cell

                # print(
                #     "POSIÇÃO VISITADA: ",
                #     maze.matrix_maze[maze.current_cell.y][maze.current_cell.x],
                #     "COORDENADAS: ",
                #     maze.current_cell.y,
                #     maze.current_cell.x,
                # )

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

    pygame.display.update()
