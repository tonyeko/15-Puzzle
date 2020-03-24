import os
import time
import copy

# constants
BLANK = 16
PUZZLE_SIZE = 16
ROW_SIZE = 4
# Global variable
plusOneIndex = [1, 3, 4, 6, 9, 11, 12, 14] #digunakan untuk X = 1 pada fungsi solvable(puzzle)
kurangList = [0 for i in range(PUZZLE_SIZE)]
# operator = ["up", "down", "left", "right"]
operator = ["up", "right", "down", "left"]
# operator = ["right", "down", "left", "up"]
final = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 ,13 ,14 ,15 , BLANK]
countNode = 0 #variabel penghitung banyak simpul yg digenerate 
queue = []
visitedNode = []
costSolution = float('inf')

class Puzzle:
    def __init__(self, state):
        self.state = state
        self.blankIndex = self.searchBlankIndex()
        self.level = 0
        self.path = []
        self.cost = self.calculateCost()
    
    def searchBlankIndex(self):
        for i in range(len(self.state)):
            if self.state[i] == BLANK: 
                return i 
    
    def print(self):
        fence = "---------------------------------"
        print(fence)
        for i in range(len(self.state)):
            value = self.state[i] if self.state[i] != BLANK else " "
            print("  ", value, end="\t|") if (i%4 != 0 or i == 0) else print("\n" + fence + "\n  ", value, end="\t|")
        print("\n" + fence + "\n")

    def calculateCost(self):
        g = 0
        for i in range(PUZZLE_SIZE):
            if final[i] != BLANK and self.state[i] != final[i]: 
                g+=1
        return self.level + g

    def isPossibleSwap(self, direction):
        indexBlank = self.searchBlankIndex()
        # change index view to 2-D array index
        rowBlank = indexBlank//ROW_SIZE
        colBlank = indexBlank%ROW_SIZE
        if direction == "up":
            rowBlank-=1
        if direction == "down":
            rowBlank+=1
        if direction == "left":
            colBlank-=1
        if direction == "right":
            colBlank+=1
        return (rowBlank >= 0 and rowBlank < 4) and (colBlank >= 0 and colBlank < 4)


def generateKurangList(startPuzzle):
    for index in range(len(startPuzzle.state)):
        value = startPuzzle.state[index]-1 #pada puzzle angkanya 1-16, pada array 0-15
        kurangList[value] = kurang(startPuzzle.state, index)
    printKurangList()

def kurang(startPuzzle, index):
    kurang = 0
    value = startPuzzle[index]
    for i in range(index+1, len(startPuzzle)):
        if startPuzzle[i] < startPuzzle[index]: kurang += 1
    return kurang

def printKurangList():
    print("=====Nilai fungsi Kurang(i)======"); print("\t i\tKurang(i)")
    print("---------------------------------")
    for index in range(len(kurangList)): 
        print("\t", index+1, "\t ", kurangList[index])

def sigmaKurangPlusX(startPuzzle):
    result = sum(kurangList)
    if startPuzzle.blankIndex in plusOneIndex:
        result+=1
    return result

def solvable(startPuzzle):
    return sigmaKurangPlusX(startPuzzle)%2==0

def popPuzzleQueue():
    global queue
    minIndex = searchMinCostElementQueue()
    item = queue[minIndex]
    del queue[minIndex]
    return item

def searchMinCostElementQueue():
    minCostIndex = 0
    for i in range(len(queue)):
        if queue[i].cost < queue[minCostIndex].cost or (queue[i].cost == queue[minCostIndex].cost and queue[i].level < queue[minCostIndex].level): # cost kurang dari atau cost sama tapi level kurang dari
            minCostIndex = i
    return minCostIndex

def solve(puzzle):
    global queue, visitedNode, countNode, costSolution
    queue.append(puzzle)
    countNode = 1
    #print start puzzle
    print("Node ke-", countNode, "(PARENT NODE) <=> Cost: ", queue[0].cost)
    queue[0].print()
    while queue != []:
        solution = popPuzzleQueue()
        visitedNode.append(solution.state)
        if (solution.cost < costSolution):
            if (solution.state == final):
                result = copy.deepcopy(solution)
                costSolution = solution.cost
            else:
                generateChildNode(solution)
    
    return result
        
        

def swapBlankPosition(puzzle, direction):
    newPuzzle = copy.deepcopy(puzzle)
    if direction == "up":
        newPuzzle.state[newPuzzle.blankIndex], newPuzzle.state[newPuzzle.blankIndex-4] = newPuzzle.state[newPuzzle.blankIndex-4], newPuzzle.state[newPuzzle.blankIndex]
    elif direction == "down":
        newPuzzle.state[newPuzzle.blankIndex], newPuzzle.state[newPuzzle.blankIndex+4] = newPuzzle.state[newPuzzle.blankIndex+4], newPuzzle.state[newPuzzle.blankIndex]
    elif direction == "left":
        newPuzzle.state[newPuzzle.blankIndex], newPuzzle.state[newPuzzle.blankIndex-1] = newPuzzle.state[newPuzzle.blankIndex-1], newPuzzle.state[newPuzzle.blankIndex]
    else: #right
        newPuzzle.state[newPuzzle.blankIndex], newPuzzle.state[newPuzzle.blankIndex+1] = newPuzzle.state[newPuzzle.blankIndex+1], newPuzzle.state[newPuzzle.blankIndex]
    newPuzzle.blankIndex = newPuzzle.searchBlankIndex()
    return newPuzzle

def generateChildNode(parentPuzzle):
    global queue, countNode
    for direction in operator:
        if parentPuzzle.isPossibleSwap(direction):
            childPuzzle = swapBlankPosition(parentPuzzle, direction)
            if childPuzzle.state not in visitedNode:
                childPuzzle.level+=1
                childPuzzle.cost = childPuzzle.calculateCost()
                childPuzzle.path = parentPuzzle.path + [parentPuzzle]
                queue.append(childPuzzle); countNode+=1
                print("Node ke-",countNode, "<=> Cost: ", childPuzzle.cost, "LEVEL: ", childPuzzle.level)
                childPuzzle.print()
    # print("Parent Node: ")
    # parentPuzzle.print()

puzzlepath = "./puzzle"
fileName = os.path.join(puzzlepath, input("File name: "))
# fileName = "3.txt"; fileName = os.path.join(puzzlepath, fileName)
file = open(fileName, "r")
start = [data for line in file for data in line.split()] #extract data from external file
start = list(map(lambda x: int(x) if x != "-" else BLANK, start)) #map to int list
puzzle = Puzzle(start)
print("=======Posisi awal Puzzle========"); 
puzzle.print()
print("=================================\n")
generateKurangList(puzzle)
print("=================================\n")
print("Sigma Kurang(i) + X = ", sigmaKurangPlusX(puzzle));  

if solvable(puzzle):
    print("Karena", sigmaKurangPlusX(puzzle), "% 2 == 0 maka puzzle : Solvable!\n")
    start_time = time.time()
    solution = solve(puzzle)
    runtime = time.time() - start_time

    print("============Jalur B&B============"); i = 1
    for o in solution.path:
        print("Jalur ke-", i, "| Level: ", o.level, "| Cost: ", o.cost)
        o.print(); i+=1
    print("Jalur ke-", i, "| Level: ", solution.level, "| Cost: ", solution.cost)
    solution.print()
    print("Runtime: %s seconds" %runtime)
    print("Jumlah simpul yang dibangkitkan:", countNode)
else:
    print("Karena", sigmaKurangPlusX(puzzle), "% 2 != 0 maka puzzle : Not Solvable!")