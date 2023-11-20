import sys
import pygame

SCREEN_SIZE = 30 # tamanho da tela 
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)

class Cell:
    def __init__(self, y, x):
        self.x = x
        self.y = y
        self.right = True
        self.left = True
        self.bottom = True
        self.top = True

    def __str__(self):
        return f"{self.x} e {self.y}"
    
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

        self.maze_stack = []  # tipo Cell

        self.width = len(maze_data[0])
        self.height = len(maze_data)

        self.current_cell = self.find_cell(self.mouse_marker)
        self.mouse_cell = self.current_cell
        self.cheese_cell = self.find_cell(self.cheese_marker)
    
    def find_cell(self, marker):
        for y in range(self.height):
            for x in range(self.width):
                if self.matrix_maze[y][x] == marker:
                    return Cell(y, x)

    def exit(self):
        # 1 Stack mazeStack;
        maze_stack = self.maze_stack;
        # 2 currentCell = posição inicial do rato;

        cell_to_move = None
        stopped = False
        left = False
        right = False
        top = False
        bottom = False

        # 3 enquanto currentCell não for exitCell faça
        while self.current_cell != self.cheese_cell:
            pygame.time.delay(3000)  # Atraso para visualização

            # 4 Marque currentCell como visitado;
            self.matrix_maze[self.current_cell.y][self.current_cell.x] = self.visited_marker  
            
            print("POSIÇÃO VISITADA: ", self.matrix_maze[self.current_cell.y][self.current_cell.x], "COORDENADAS: ", self.current_cell.y, self.current_cell.x)

            # 5 Coloque na pilha os vizinhos não-visitados de currentCell;
            if self.matrix_maze[self.current_cell.y][self.current_cell.x + 1] != self.wall_marker and self.matrix_maze[self.current_cell.y][self.current_cell.x + 1] != self.visited_marker:
                right = True
                print('RIGHT')
                cell_to_move = Cell(self.current_cell.y, (self.current_cell.x + 1))
                self.maze_stack.append(cell_to_move)

            elif self.matrix_maze[self.current_cell.y][self.current_cell.x - 1] != self.wall_marker and self.matrix_maze[self.current_cell.y][self.current_cell.x - 1] != self.visited_marker:
                left = True
                print('LEFT')
                cell_to_move = Cell(self.current_cell.y, (self.current_cell.x - 1))
                self.maze_stack.append(cell_to_move)

            elif self.matrix_maze[self.current_cell.y + 1][self.current_cell.x] != self.wall_marker and self.matrix_maze[self.current_cell.y + 1][self.current_cell.x] != self.visited_marker:
                bottom = True
                print('BOTTOM')
                cell_to_move = Cell((self.current_cell.y + 1), self.current_cell.x)
                self.maze_stack.append(cell_to_move)
            
            elif self.matrix_maze[self.current_cell.y - 1][self.current_cell.x] != self.wall_marker and self.matrix_maze[self.current_cell.y - 1][self.current_cell.x] != self.visited_marker: 
                top = True
                print('TOP')
                cell_to_move = Cell((self.current_cell.y - 1), self.current_cell.x)
                self.maze_stack.append(cell_to_move)
            
    
            # Fazer o rato andar # esquerda direita cima baixo cima
            # A POSIÇÃO DE VOLTA SERÁ SEMPRE ONDE TEM + DE 2 FLAGS(ex. left e right)
            if right and self.current_cell.right == True:
                draw_maze(screen, self)
                self.current_cell.right = False
                self.current_cell = cell_to_move
                for maze in maze_stack:
                    print(maze)
                    
            elif left and self.current_cell.left == True:
                draw_maze(screen, self)
                self.current_cell.left = False
                self.current_cell = cell_to_move
                for maze in maze_stack:
                    print(maze)

            elif bottom and self.current_cell.bottom == True:
                draw_maze(screen, self)
                self.current_cell.bottom = False
                self.current_cell = cell_to_move   
                for maze in maze_stack:
                    print(maze)

            elif top and self.current_cell.top == True:
                draw_maze(screen, self)
                self.current_cell.top = False
                self.current_cell = cell_to_move 
                for maze in maze_stack:
                    print(maze)

            # 6 se A pilha mazeStack estiver vazia então
            if len(maze_stack) == 0:
                # 7 caminho não encontrado;
                print('Caminho não encontrado')                
            # 8 senão
            else:
                # 9 Faça um pop na pilha e o faça currentCell;
                self.current_cell = self.maze_stack.pop()
                # print( "CURRENT", self.current_cell )
                print("Achou o caminho")
        
            # print( "CHEESE", self.cheese_cell)
            # print( "CURRENT", self.current_cell )
            print( "IGUAL??", self.current_cell == self.cheese_cell)
            
            # CONFERIR ESSA MAZE_STACK AGORA, TEMQ TER O CAMINHO DO QUEIJO AO RATO
            # PINTAR OS QUADRADOS DA COR CERTA
            for maze in maze_stack:
                print(maze)

        
        # 10 fim
    # 11 fim

# while len(maze_stack) > 0: 
# self.current_cell = cell_to_move
# maze.matrix_maze[maze.mouse_cell.y][maze.mouse_cell.x] = maze.cheese_marker
# maze.mouse_cell.y = cell_to_move.y
# maze.mouse_cell.x = cell_to_move.x
# maze.matrix_maze[cell_to_move.x][cell_to_move.y] = maze.mouse_marker



def load_txt_maze(file_name):
    with open(file_name, 'r') as file_txt:
        stack_load_txt_maze = []

        # Enquanto houver linhas para serem lidas faça
        for line in file_txt:
            # Adicionar paredes nas extremidades
            line = '1' + line.strip() + '1' 
            # Fazer um push na pilha
            stack_load_txt_maze.append(line) # strip para tirar o /n
        
        maze_rows = []
        # Armazenar a primeira linha em uma variável
        first_line = stack_load_txt_maze[0]
        # Adicionar em maze_rows a primeira linha de paredes
        maze_rows.append('1' * len(first_line))
        # Realizar pops na pilha adicionando em maze_rows
        while stack_load_txt_maze:
            popped_line = stack_load_txt_maze.pop(0)
            maze_rows.append(popped_line)
        # Adicionar em maze a última linha de paredes
        maze_rows.append('1' * len(first_line))
        # Transformando em uma matriz
        maze_2d = [list(line) for line in maze_rows]

        return maze_2d


def draw_maze(screen, maze):
    # Limpar a tela com uma cor sólida (nesse caso, preto)
    screen.fill((255, 0, 0))

    for y in range(maze.height): # linhas
        for x in range(maze.width): # colunas

                                #    coordenada x   coordenada y    width        height
            square = pygame.Rect(x * SCREEN_SIZE, y * SCREEN_SIZE, SCREEN_SIZE, SCREEN_SIZE)

            if maze.matrix_maze[y][x] == maze.wall_marker:
                pygame.draw.rect(screen, GRAY, square)
                
            elif maze.matrix_maze[y][x] == maze.passage_marker:
                pygame.draw.rect(screen, WHITE, square)

            elif maze.matrix_maze[y][x] == maze.mouse_marker :
                pygame.draw.rect(screen, (0,0,0), square)
                screen.blit(mouse_image, square)  # Adiciona a imagem na posição 

            elif maze.matrix_maze[y][x] == maze.cheese_marker:
                pygame.draw.rect(screen, (0,0,0), square)
                screen.blit(cheese_image, square)

    pygame.display.flip() 

def keydown_mouse(maze):
    move_action = False
    
    new_mouse_position_y = maze.mouse_cell.y
    new_mouse_position_x = maze.mouse_cell.x

    if event.type == pygame.KEYDOWN:
        move_action = True

        if event.key == pygame.K_LEFT:
            if maze.matrix_maze[maze.mouse_cell.y][maze.mouse_cell.x - 1] != maze.wall_marker: 
                print('left')
                new_mouse_position_x -= 1
                # pygame.time.delay(300) # delay para usar
        elif event.key == pygame.K_RIGHT:
            if maze.matrix_maze[maze.mouse_cell.y][maze.mouse_cell.x + 1] != maze.wall_marker:
                new_mouse_position_x += 1  
                print('right')
        elif event.key == pygame.K_UP:
            if maze.matrix_maze[maze.mouse_cell.y - 1][maze.mouse_cell.x] != maze.wall_marker:
                new_mouse_position_y -= 1  
                print('up')
        elif event.key == pygame.K_DOWN:
            if maze.matrix_maze[maze.mouse_cell.y + 1][maze.mouse_cell.x] != maze.wall_marker:
                new_mouse_position_y += 1 
                print('down')

        if move_action:
            move_action = False
            
            print('mouse_position_y', maze.mouse_cell.y) 
            print('mouse_position_x', maze.mouse_cell.x) 
            
            # Atualizando a posição do rato
            maze.matrix_maze[maze.mouse_cell.y][maze.mouse_cell.x] = maze.passage_marker
            maze.mouse_cell.x, maze.mouse_cell.y = new_mouse_position_x, new_mouse_position_y
            maze.matrix_maze[new_mouse_position_y][new_mouse_position_x] = maze.mouse_marker

# MAIN

pygame.init() # obrigatório?

# Para carregar as imagens
mouse_image = pygame.image.load('imgs/rato.gif')
cheese_image = pygame.image.load('imgs/cheese.gif')
                                                    # width       height
cheese_image = pygame.transform.scale(cheese_image, (SCREEN_SIZE, SCREEN_SIZE))


# ALGORITMO 1 - INICIALIZAR LABIRINTO

# Carregando labirinto
maze = Maze(load_txt_maze('maze3.txt'))

# Configurações da Tela
screen = pygame.display.set_mode((maze.width * SCREEN_SIZE, maze.height * SCREEN_SIZE))
pygame.display.set_caption('Mouse&Cheese Maze')

# Iniciando o Pygame
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keydown_mouse(maze)

    draw_maze(screen, maze)

    # maze.exit()


pygame.quit() # obrigatório?
sys.exit() # obrigatório?

    # 
# def exit(self):
#     maze_stack = self.maze_stack
#     current_cell = self.current_cell

#     def move(direction):
#         nonlocal current_cell
#         if direction == "esquerda":
#             current_cell = Cell(current_cell.y, current_cell.x - 1)
#         elif direction == "direita":
#             current_cell = Cell(current_cell.y, current_cell.x + 1)
#         elif direction == "baixo":
#             current_cell = Cell(current_cell.y + 1, current_cell.x)
#         elif direction == "cima":
#             current_cell = Cell(current_cell.y - 1, current_cell.x)

#     priority_order = ["esquerda", "direita", "baixo", "cima"]

#     while current_cell != self.cheese_cell:
#         pygame.time.delay(200)  # Delay for visualization
#         self.matrix_maze[current_cell.y][current_cell.x] = self.visited_marker

#         for direction in priority_order:
#             if (direction == "esquerda" and self.matrix_maze[current_cell.y][current_cell.x - 1] == self.passage_marker) or \
#                (direction == "direita" and self.matrix_maze[current_cell.y][current_cell.x + 1] == self.passage_marker) or \
#                (direction == "baixo" and self.matrix_maze[current_cell.y + 1][current_cell.x] == self.passage_marker) or \
#                (direction == "cima" and self.matrix_maze[current_cell.y - 1][current_cell.x] == self.passage_marker):
#                 move(direction)
#                 draw_maze(screen, self)
#                 break
#         else:
#             if len(maze_stack) == 0:
#                 print('Caminho não encontrado')
#                 break
#             else:
#                 self.current_cell = self.maze_stack.pop()
#                 print("Achou o caminho")