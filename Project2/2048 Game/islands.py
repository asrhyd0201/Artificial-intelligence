#!/usr/bin/python3

def islands(grid):
    
    island = 0
    visited = []
    for i in range(0,4):
        rows = []
        for j in range(0,4):
            rows.append(0)
        visited.append(rows)    
    
    for i in range(0,4):
        for j in range(0,4):
            if grid[i][j] != 0 and visited[i][j] == 0:
                dfs(grid, i, j, visited) 
                island = island + 1
    return island
        
def dfs(grid, row, col, visited):    
    
    x = [-1, 0, 1, 0]
    y = [0, 1, 0, -1]    
    visited[row][col] = 1 
    for ele in range(0,4):
        newX = x[ele] + row
        newY = y[ele] + col
        if(valid(grid, newX, newY, visited)):
            dfs(grid, newX, newY, visited)                        
            
def valid(grid, row, col, visited):
    
    if(row >= 0 and row < 4 and col >= 0 and col < 4 and grid[row][col] != 0 and visited[row][col] == 0):
        return True
    return False    
    
def printf(matrix):

    for i in matrix:
        row = ""
        for j in i:
            row = row + str(j) + " "    
        print(row)        
        
if __name__ == '__main__':

    grid = [[4, 2, 0, 0], [2, 0, 0, 0], [0, 0, 4, 2], [2, 0, 2, 4]]
    print (islands(grid))
