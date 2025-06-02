from django.shortcuts import render
import random

def home(request):
    grid_size = 10
    rows = grid_size
    cols = grid_size
    
    start_col = random.randint(0, cols - 1)
    path = [start_col]
    visited = set(path)
    
    current = start_col
    current_row = 0
    
    while current_row < rows - 1:
        possible_moves = []
        
        if current_row < rows - 1:
            down = current + cols
            if down not in visited:
                possible_moves.append(down)
        
        left = current - 1
        if (left not in visited and 
            left // cols == current_row and 
            left >= current_row * cols):
            possible_moves.append(left)
            
        right = current + 1
        if (right not in visited and 
            right // cols == current_row and 
            right < (current_row + 1) * cols):
            possible_moves.append(right)
        
        valid_moves = []
        for move in possible_moves:
            safe = True
            
            if move == current + cols: 
                if (current - 1 in visited and 
                    move - 1 in visited and 
                    current - 1 - cols in visited):
                    safe = False

                if (current + 1 in visited and 
                    move + 1 in visited and 
                    current + 1 - cols in visited):
                    safe = False
                        
            elif move == current - 1: 
                if (current - cols in visited and 
                    move - cols in visited and 
                    current - cols - 1 in visited):
                    safe = False
                        
            elif move == current + 1: 
                if (current - cols in visited and 
                    move - cols in visited and 
                    current - cols + 1 in visited):
                    safe = False
            
            if safe:
                valid_moves.append(move)
        
        if valid_moves:
            down_moves = [m for m in valid_moves if m == current + cols]
            if down_moves and random.random() < 0.7:
                next_cell = down_moves[0]
            else:
                next_cell = random.choice(valid_moves)
            
            path.append(next_cell)
            visited.add(next_cell)
            current = next_cell
            current_row = current // cols
      
        else:
            if len(path) > 1:
                path.pop()
                current = path[-1]
                current_row = current // cols
            else:
                return home(request)
    
    return render(request, 'game/home.html', {
        'path': path,
        'grid_size': grid_size
    })
