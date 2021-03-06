from random import randint
from BaseAI import BaseAI
import sys 
import math
import time

class PlayerAI(BaseAI):
   
    def heuristicFunction(self, grid):
        
        monotonicityWeight = 1
        smoothnessWeight = 0.1
        emptyWeight  = 2.7
        maxWeight    = 1
        cornerWeight = 1.5
        
        num_blank = len(grid.getAvailableCells())
        max_tile = grid.getMaxTile()
        if num_blank == 0:
            return math.log(max_tile, 2) - 100
        
        monoticity = self.getMonotonic(grid)
        smoothness = self.getSmoothness(grid)

        return monotonicityWeight * monoticity + smoothnessWeight * smoothness \
        + emptyWeight * num_blank \
        + maxWeight * max_tile 
        #+ cornerWeight * self.getCornerMaxElement(grid)
   
    def cellOccupied(self, grid, x, y):
        
        pos = []
        pos.append(x)
        pos.append(y)
        if grid.getCellValue(pos):
            return True
        else:
            return False 
        
    def getMonotonic(self, grid):
        
        result = [0,0,0,0]

        for x in range(0,4):
            currY = 0
            nextY = currY + 1

            while nextY < 4:
                while nextY < 4 and not self.cellOccupied(grid, x, nextY):
                    nextY = nextY + 1
                if nextY >= 4:
                    nextY = nextY - 1
                cPos = []
                nPos = []
                cPos.append(x)
                cPos.append(currY)
                nPos.append(x)
                nPos.append(nextY)
                currValue = math.log(grid.getCellValue(cPos)) / math.log(2) if grid.getCellValue(cPos) else 0
                nextValue = math.log(grid.getCellValue(nPos)) / math.log(2) if grid.getCellValue(nPos) else 0
                if currValue > nextValue:
                    result[0] += (nextValue - currValue)
                if nextValue > currValue:
                    result[1] += (currValue - nextValue)
                currY = nextY
                nextY = currY + 1

        for y in range(0,4):
            currX = 0
            nextX = currX + 1

            while nextX < 4:
                while nextX < 4 and not self.cellOccupied(grid, nextX, y):
                    nextX = nextX + 1
                if nextX >= 4:
                    nextX = nextX - 1
                cPos = []
                nPos = []
                cPos.append(currX)
                cPos.append(y)
                nPos.append(nextX)
                nPos.append(y)
                currValue = math.log(grid.getCellValue(cPos)) / math.log(2) if grid.getCellValue(cPos) else 0 
                nextValue = math.log(grid.getCellValue(nPos)) / math.log(2) if grid.getCellValue(nPos) else 0
                if currValue > nextValue:
                    result[2] += (nextValue - currValue)
                if nextValue > currValue:
                    result[3] += (currValue - nextValue)
                currX = nextX
                nextX = currX + 1

        return max(result[0], result[1]) + max(result[2], result[3])

    def getSmoothness(self, grid):
                    
        direction = [[1, 0],[0, 1]]     
        smoothness = 0

        for x in range(0,4) :
            for y in range(0,4):
                cell = [x, y]
                if grid.getCellValue(cell):

                    for dir in direction:
                        farthestCell = self.findFarthestCell(grid, cell, dir)
                        if grid.getCellValue(farthestCell):
                            
                            cellVal = math.log(grid.getCellValue(cell)) / math.log(2)
                            farVal = math.log(grid.getCellValue(farthestCell)) / math.log(2)
                            smoothness += abs(cellVal-farVal)
                    
        return smoothness                    
               
    def findFarthestCell(self, grid, cell, dir):    
        
        previousCell = cell
        nextCell = [ previousCell[0]+dir[0], previousCell[1]+dir[1] ]
        while nextCell[0] >= 0 and nextCell[1] < 4 and grid.getCellValue(nextCell):
            nextCell = [ previousCell[0]+dir[0], previousCell[1]+dir[1] ]
            previousCell = nextCell
        return nextCell
   
    def getCornerMaxElement(self, grid):
       
        leftTop     = [0, 0]
        rightTop    = [0, 3]
        leftBottom  = [3, 0]
        rightBottom = [3, 0]
        maxEle = grid.getMaxTile()

        leftTopVal     = grid.getCellValue(leftTop)
        rightTopVal    = grid.getCellValue(rightTop)
        leftBottomVal  = grid.getCellValue(leftBottom)
        rightBottomVal = grid.getCellValue(rightBottom)

        if maxEle == leftTopVal or maxEle == rightTopVal or maxEle == leftBottomVal or maxEle == rightBottomVal:
            return math.log(maxEle) / math.log(2)
        return 0
        
     
    def getMove(self, grid):
       
        depth = 3
        prev = time.clock()
        move = self.maximize(grid, depth, float('-inf'), float('inf'))
        curr = time.clock()
        print ("Alpha Beta Time", curr-prev)
        return move[1]
     
    def maximize(self, grid, depth, alpha, beta):
      
        if(depth <= 0 or not grid.canMove()):
            score = self.heuristicFunction(grid)
            return (score, None)
        moves = grid.getAvailableMoves()
        bestMove = moves[0]
        for m in moves:
            newGrid = grid.clone()
            newGrid.move(m)
            resultScore, resultMove = self.minimize(newGrid, depth-1, alpha, beta)
            if resultScore > alpha:
                alpha = resultScore
                bestMove = m
            if resultScore >= beta:
                break
        return (alpha, bestMove)
    
    def minimize(self, grid, depth, alpha, beta):
        
        moves = grid.getAvailableCells()
        for m in moves:
            newGrid = grid.clone()
            newGrid.insertTile(m, 2)
            resultScore, resultMove = self.maximize(newGrid, depth-1, alpha, beta)
            if resultScore < beta:
                beta = resultScore
            if resultScore <= alpha:
                break
        return (beta, None)
