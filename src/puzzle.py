import os
import time
import copy
import heapq

# constants
BLANK = 16
PUZZLE_SIZE = 16
ROW_SIZE = 4
# Global variable
plusOneIndex = [1, 3, 4, 6, 9, 11, 12, 14] #digunakan untuk X = 1 pada fungsi solvable(puzzle)
kurangList = [0 for i in range(PUZZLE_SIZE)]
operator = ["up", "down", "left", "right"]
final = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 ,13 ,14 ,15 , BLANK]
countNode = 0 #variabel penghitung banyak simpul yg digenerate 
queue = []
visitedNode = set()
costSolution = float('inf') #inisiasi cost untuk solusi

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
    print("=====Nilai fungsi Kurang(i)======")
    print("\t i\tKurang(i)")
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

def solve(puzzle):
    global queue, visitedNode, countNode, costSolution
    countNode = 1
    heapq.heappush(queue, (puzzle.cost, -1*countNode, puzzle))
    while queue != []:
        # solution = popPuzzleQueue()
        solution = heapq.heappop(queue)[2]
        visitedNode.add(tuple(solution.state))
        if (solution.cost < costSolution): #berfungsi untuk membunuh simpul yang costnya > simpul solusi setelah simpul solusi ditemukan
            if (solution.state == final):
                result = copy.deepcopy(solution)
                costSolution = solution.cost
            else:
                generateChildNode(solution)
    return result
        

def swapBlankPosition(puzzle, direction):
    newPuzzle = copy.deepcopy(puzzle)
    indexBlank = newPuzzle.blankIndex
    if direction == "up":
        newBlankIndex = indexBlank-4
    elif direction == "down":
        newBlankIndex = indexBlank+4
    elif direction == "left":
        newBlankIndex = indexBlank-1
    else: #right
        newBlankIndex = indexBlank+1
    newPuzzle.state[indexBlank], newPuzzle.state[newBlankIndex] = newPuzzle.state[newBlankIndex], newPuzzle.state[indexBlank]
    newPuzzle.blankIndex = newBlankIndex
    return newPuzzle

def createNewState(state, direction, blankIndex):
    newState = copy.deepcopy(state)
    indexBlank = blankIndex
    if direction == "up":
        newBlankIndex = indexBlank-4
    elif direction == "down":
        newBlankIndex = indexBlank+4
    elif direction == "left":
        newBlankIndex = indexBlank-1
    else: #right
        newBlankIndex = indexBlank+1
    newState[indexBlank], newState[newBlankIndex] = newState[newBlankIndex], newState[indexBlank]
    return (newState, newBlankIndex)

def createNewPuzzle(parentPuzzle, currentState, currentBlankIndex):
    global countNode
    newPuzzle = copy.deepcopy(parentPuzzle)
    newPuzzle.state = currentState
    newPuzzle.blankIndex = currentBlankIndex
    newPuzzle.level+=1
    newPuzzle.cost = newPuzzle.calculateCost()
    newPuzzle.path = parentPuzzle.path + [parentPuzzle]
    countNode+=1
    return newPuzzle


def generateChildNode(parentPuzzle):
    global queue, countNode
    for direction in operator:
        if parentPuzzle.isPossibleSwap(direction):
            childPuzzleState = createNewState(parentPuzzle.state, direction, parentPuzzle.blankIndex)
            if tuple(childPuzzleState[0]) not in visitedNode:
                childPuzzle = createNewPuzzle(parentPuzzle, childPuzzleState[0], childPuzzleState[1]) 
                heapq.heappush(queue, (childPuzzle.cost, -1*countNode, childPuzzle))


puzzlepath = "../test" 
fileName = os.path.join(puzzlepath, input("File name: "))
file = open(fileName, "r")
start = [data for line in file for data in line.split()] #extract data from external file
start = list(map(lambda x: int(x) if x != "-" else BLANK, start)) #map to int list
puzzle = Puzzle(start)
print("=======Posisi awal Puzzle========")
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
        print("Jalur ke-"+str(i), "| Level: ", o.level, "| Cost: ", o.cost)
        o.print(); i+=1
    print("Goal Node | Level: ", solution.level, "| Cost: ", solution.cost)
    solution.print()
    print("Runtime: %s seconds" %runtime)
    print("Jumlah simpul yang dibangkitkan:", countNode)
else:
    print("Karena", sigmaKurangPlusX(puzzle), "% 2 != 0 maka puzzle : Not Solvable!")