#!/usr/bin/python3
import sys
import collections
from traceback import print_exc
import resource
import timeit
import copy
import heapq

class EightPuzzle(Exception):


    # Parsing the command line arguments
    def parseCommandLineArgs(self,args):
       
        if(len(args) < 2):
            print ('Usage: driver_3.py <method> <board>')  
            sys.exit(1)
        else:    
            method = args[0]
            board  = args[1]
            if method == "bfs":
                bfs = BfsSolver()
                bfs.search8Puzzle(board.split(",")) 
            elif method == "dfs":
                dfs = DfsSolver()
                dfs.search8Puzzle(board.split(","))
            elif method == "ast":
                ast = AstarSolver()
                ast.search8Puzzle(board.split(","))

class Board(Exception):


    def __init__(self, board):
        self.board = board
    
    # Finds the empty tile and 
    # return the tile index in 
    # the list

    def emptyTile(self):
        count = 0
        for ele in self.board:
            if ele == str(0):
                return count
            count = count + 1
        return -1
    
    def swapEmptyTile(self, emptyTileIndex, pos):
        temp = self.board[emptyTileIndex]
        self.board[emptyTileIndex] = self.board[pos]
        self.board[pos] = temp
        
    def getBoard(self):
        return self.board

    def setBoard(self, board):
        self.board = board

    def manDist(self):

        dist = 0
        for index, value in enumerate(self.board):
            if(value == -1):
                continue
            diff = abs(index - int(value))
            dist += (diff / 3) + (diff % 3)
        return dist

    def getBoardKey(self):
        return ''.join(self.board)

class State:
    

    goal = [
            '0', '1', '2', 
            '3', '4', '5', 
            '6', '7', '8'
           ]
    
    def __init__(self, boardObj, parent = None, gCost = 0, hCost = 0, fCost = 0, operation = '', depth = 0):

        self.boardObj = boardObj
        self.parent = parent
        self.cost = gCost
        self.hCost = hCost
        self.fCost = fCost
        self.operation = operation   
        self.depth = depth     

    def genSuccessor(self):    
        emptyTileIndex = self.getBoardObject().emptyTile()
        successorList = [] 
        tempBoard = self.getBoardObject().getBoard()
        # UP    
        if emptyTileIndex != 0 and emptyTileIndex != 1 and emptyTileIndex != 2:
            b = Board(list(tempBoard))
            b.swapEmptyTile(emptyTileIndex, emptyTileIndex-3)
            gCost = self.getCost() + 1
            hCost = b.manDist()
            fCost = gCost + hCost
            successorList.append(State(b, self, gCost, hCost, fCost, 'Up', self.getDepth()+1))
        # DOWN
        if emptyTileIndex != 6 and emptyTileIndex != 7 and emptyTileIndex != 8:
            b = Board(list(tempBoard))
            b.swapEmptyTile(emptyTileIndex, emptyTileIndex+3)
            gCost = self.getCost() + 1
            hCost = b.manDist()
            fCost = gCost + hCost
            successorList.append(State(b, self, gCost, hCost, fCost, 'Down', self.getDepth()+1))
        # LEFT
        if emptyTileIndex != 0 and emptyTileIndex != 3 and emptyTileIndex != 6: 
            b = Board(list(tempBoard))
            b.swapEmptyTile(emptyTileIndex, emptyTileIndex-1)
            gCost = self.getCost() + 1
            hCost = b.manDist()
            fCost = gCost + hCost
            successorList.append(State(b, self, gCost, hCost, fCost, 'Left', self.getDepth()+1))            
        # RIGHT
        if emptyTileIndex != 2 and emptyTileIndex != 5 and emptyTileIndex != 8:
            b = Board(list(tempBoard))
            b.swapEmptyTile(emptyTileIndex, emptyTileIndex+1)
            gCost = self.getCost() + 1
            hCost = b.manDist()
            fCost = gCost + hCost
            successorList.append(State(b, self, gCost, hCost, fCost, 'Right', self.getDepth()+1))
      
        return successorList
   
    def __lt__(self, other):
        return self.fCost < other.fCost

    def getCost(self):
        return self.cost

    def getHCost(self):
        return self.hCost
    
    def getFCost(self):
        return self.fCost

    def getDepth(self):
        return self.depth

    def getOperation(self):    
        return self.operation

    def getCurrBoard(self):
        return self.boardObj.getBoard()
    
    def getCurrBoardString(self):
        return ''.join(self.boardObj.getBoard())
       
    def printCurrBoard(self):
        s = ""
        board = self.boardObj.getBoard()
        s = s + board[0] + "|" + board[1] + "|" + board[2] + "\n"
        s = s + board[3] + "|" + board[4] + "|" + board[5] + "\n"
        s = s + board[6] + "|" + board[7] + "|" + board[8] + "\n"
        return s
 
    def getBoardObject(self):
        return self.boardObj

    def getParent(self):
        return self.parent
    
    def printSuccessorList(self, succ):
        s = ""
        for i in succ:
            s = s + "[" + str(i.getCurrBoard()) + "],  " 
        return s

    def isGoal(self):
        """ check if the current 
            state is goal state 
            or not 
        """
        for index in range(9): 
            if self.getCurrBoard()[index] == self.goal[index]:
                continue
            else:
                return False
        return True
 
class QueueFrontier:


    def __init__(self):
        self.dict = collections.OrderedDict()
 
    def isEmpty(self):
        if not self.dict:
            return True
        else:
            return False
         
    def add(self,state):
        key = state.getCurrBoardString()
        self.dict[key] = state
        
    def remove(self):
        if not self.dict:
            raise Exception('No eLements in dictionary!'
            'May be board argument is not passed')
        firstElement = self.dict.popitem(last = False)
        return firstElement[1]        
        
    def checkState(self, state):
        key = state.getCurrBoardString()
        if key in self.dict:
            return True

        else:
            return False
            
class BfsSolver:


    def __init__(self):
        self.qFrontier = QueueFrontier()
        self.visitedBoards = set()
        self.maxSearchDepth = 0
        self.expandedNodes = 0

    def search8Puzzle(self, board):
        """ search 8 puzzle to reach 
            goal state 
        """
        start = timeit.default_timer()
        root = State(Board(board))
        self.qFrontier.add(root) 
        self.visitedBoards.add(root.getCurrBoardString())

        while not self.qFrontier.isEmpty():
            currState = self.qFrontier.remove()
            self.visitedBoards.add(currState.getCurrBoardString())
            if currState.getDepth() > self.maxSearchDepth:
                self.maxSearchDepth = currState.getDepth()

            if(currState.isGoal()):
                stop = timeit.default_timer()
                goalPath = self.findPath(currState)
                costPath = currState.getCost()
                expandedNodes = self.expandedNodes
                searchDepth = currState.getDepth()
                maxSearchDepth = self.maxSearchDepth + 1
                runTime = (stop - start) / 3600
                memoryUsage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                out = OutPutting("output.txt")
                out.writeToFile(goalPath, costPath, expandedNodes,searchDepth,
                                 maxSearchDepth, runTime, memoryUsage)  
                break

            else:
                listOfStates = []
                self.expandedNodes = self.expandedNodes + 1
                listOfStates = currState.genSuccessor()

                for state in listOfStates:
                    if not self.checkVisitedBoards(state) and not self.qFrontier.checkState(state):
                        self.qFrontier.add(state)

    def checkVisitedBoards(self, state):
        element = state.getCurrBoardString()
        if element in self.visitedBoards:
            return True
        else:
            return False
           
    def findPath(self, state):
        
        path = []
        while state != None :
            path.append(state.getOperation())    
            state = state.getParent()  
        path = path[0 : len(path)-1] 
        return path[::-1]


class StackFrontier:
    

    def __init__(self):
        self.stack = []
        self.stackSet = set()

    def isEmpty(self):
        if not self.stack:
            return True
        else:
            return False

    def push(self,state):
        key = state.getCurrBoardString()
        self.stackSet.add(key)
        self.stack.append(state)

    def pop(self):
        if not self.stack:
            raise Exception('No eLements in Stack!'
            'May be board argument is not passed')
        lastElement = self.stack.pop()
        key = lastElement.getCurrBoardString()
        if key in self.stackSet:
            self.stackSet.remove(key)
        return lastElement

    def checkState(self, state):
        key = state.getCurrBoardString()
        if key in self.stackSet:
            return True
        else:
            return False

    def getStackFrontier(self):
        return self.stack
    

class DfsSolver:


    def __init__(self):
        self.sFrontier = StackFrontier()
        self.visitedBoards = set()
        self.maxSearchDepth = 0
        self.expandedNodes = 0

    def search8Puzzle(self, board):
        """ search 8 puzzle to reach 
            goal state 
        """
        start = timeit.default_timer()
        root = State(Board(board))
        self.sFrontier.push(root)
        self.visitedBoards.add(root.getCurrBoardString())
        while not self.sFrontier.isEmpty():

            currState = self.sFrontier.pop()
            if currState.getDepth() > self.maxSearchDepth:
                self.maxSearchDepth = currState.getDepth()

            if(currState.isGoal()):
                stop = timeit.default_timer()
                goalPath = self.findPath(currState)
                costPath = currState.getCost()
                expandedNodes = self.expandedNodes
                searchDepth = currState.getDepth()
                maxSearchDepth = self.maxSearchDepth
                runTime = (stop - start)
                memoryUsage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                out = OutPutting("output.txt")
                out.writeToFile(goalPath, costPath, expandedNodes, searchDepth, 
                                maxSearchDepth, runTime, memoryUsage)
                break

            else:
                listOfStates = []
                self.expandedNodes = self.expandedNodes + 1
                listOfStates = currState.genSuccessor()
                listOfStates = listOfStates[::-1]
                self.visitedBoards.add(currState.getCurrBoardString())
                for state in listOfStates:
                    if not self.checkVisitedBoards(state) and not self.sFrontier.checkState(state):
                        self.sFrontier.push(state)

    def checkVisitedBoards(self, state):
        element = state.getCurrBoardString()
        if element in self.visitedBoards:
            return True
        else:
            return False

    def findPath(self, state):

        path = []
        while state != None :
            path.append(state.getOperation())
            state = state.getParent()
        path = path[0 : len(path)-1]
        return path[::-1]


class HeapFrontier:
    

    def __init__(self):
        self.heap = []
        self.heapSet = set()

    def isEmpty(self):
        if not self.heap:
            return True
        else:
            return False

    def insert(self,state):
        key = state.getCurrBoardString()
        self.heapSet.add(key)
        heapq.heappush(self.heap, state)

    def deleteMin(self):
        if not self.heap:
            raise Exception('No eLements in Stack!'
            'May be board argument is not passed')
        minElement = heapq.heappop(self.heap)
        key = minElement.getCurrBoardString()
        if key in self.heapSet:
            self.heapSet.remove(key)
        return minElement

    def parent(self, i):
        return (i-1)/2

    def decreaseKey(self, state):
        
        loc = self.findStateLocation(state)
        if loc == -1:
            return -1
        parentLoc = int(self.parent(loc))
        if(state.getFCost() < self.heap[loc].getFCost()):
            self.heap[loc] = state
            while(loc != 0 and self.heap[parentLoc] > self.heap[loc]): 
                self.heap[loc] , self.heap[parentLoc] = (
                self.heap[parentLoc], self.heap[loc])
                loc = parentLoc
                parentLoc = int(self.parent(loc))
                
                
    def findStateLocation(self, state):
        for index, currState in enumerate(self.heap):
            if currState.getCurrBoardString() == state.getCurrBoardString():
                return index    
        return -1    
            
    def checkState(self, state):
        key = state.getCurrBoardString()
        if key in self.heapSet:
            return True
        else:
            return False

    def getHeapFrontier(self):
        return self.heap

class AstarSolver:


    def __init__(self):
        self.hFrontier = HeapFrontier()
        self.visitedBoards = set()
        self.maxSearchDepth = 0
        self.expandedNodes = 0

    def search8Puzzle(self, board):
        """ search 8 puzzle to reach 
            goal state 
        """
        start = timeit.default_timer()
        root = State(Board(board))
        self.hFrontier.insert(root)
        self.visitedBoards.add(root.getCurrBoardString())
        while not self.hFrontier.isEmpty():

            currState = self.hFrontier.deleteMin()
            if currState.getDepth() > self.maxSearchDepth:
                self.maxSearchDepth = currState.getDepth()

            if(currState.isGoal()):
                stop = timeit.default_timer()
                goalPath = self.findPath(currState)
                costPath = currState.getCost()
                expandedNodes = self.expandedNodes
                searchDepth = currState.getDepth()
                maxSearchDepth = self.maxSearchDepth
                runTime = (stop - start)
                memoryUsage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                out = OutPutting("output.txt")
                out.writeToFile(goalPath, costPath, expandedNodes, searchDepth,
                                maxSearchDepth, runTime, memoryUsage)
                break

            else:
                listOfStates = []
                self.expandedNodes = self.expandedNodes + 1
                listOfStates = currState.genSuccessor()
                self.visitedBoards.add(currState.getCurrBoardString())
                for state in listOfStates:
                    if not self.checkVisitedBoards(state) and not self.hFrontier.checkState(state):
                        self.hFrontier.insert(state)
                    if self.hFrontier.checkState(state):
                        self.hFrontier.decreaseKey(state)

    def checkVisitedBoards(self, state):
        element = state.getCurrBoardString()
        if element in self.visitedBoards:
            return True
        else:
            return False

    def findPath(self, state):

        path = []
        while state != None :
            path.append(state.getOperation())
            state = state.getParent()
        path = path[0 : len(path)-1]
        return path[::-1]

            
class OutPutting:


    def __init__(self, fileName):
        self.out = open(fileName,"w")

    def writeToFile(self, goalPath, costPath, expandedNodes, searchDepth, maxSearchDepth, runTime, memoryUsage):
        self.out.write("path_to_goal: " + str(goalPath) + "\n")
        self.out.write("cost_of_path: " + str(costPath) + "\n")
        self.out.write("nodes_expanded: " + str(expandedNodes) + "\n")
        self.out.write("search_depth: " + str(searchDepth) + "\n")
        self.out.write("max_search_depth: " + str(maxSearchDepth) + "\n")
        self.out.write("running_time: " + str(runTime) + "\n")
        self.out.write("max_ram_usage: " + str(memoryUsage) + "\n")
        self.out.close()

# Main Program
if __name__ == '__main__':

    try:
        ep = EightPuzzle()
        ep.parseCommandLineArgs(sys.argv[1:])

    except Exception as e:
        print ("Exception occured is:", e.__class__.__name__)
        print_exc()
