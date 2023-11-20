def load_txt_maze(file_name):
    with open(file_name, 'r') as file_txt:
        stack_load_txt_maze = []

        # to add the walls on the sides
        for line in file_txt:
            
            line = '1' + line.strip() + '1' 

            stack_load_txt_maze.append(line)  
        
        # to add the walls top and bottom
        maze_rows = [] 
         
        first_line = stack_load_txt_maze[0]
         
        maze_rows.append('1' * len(first_line))
         
        while stack_load_txt_maze:
            popped_line = stack_load_txt_maze.pop(0)
            maze_rows.append(popped_line)
         
        maze_rows.append('1' * len(first_line))
        
        maze_2d = [list(line) for line in maze_rows]

        return maze_2d
