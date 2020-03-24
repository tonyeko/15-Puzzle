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
# operator = ["up", "right", "down", "left"]
operator = ["right", "down", "left", "up"]
final = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 ,13 ,14 ,15 , BLANK]
countNode = 0 #variabel penghitung banyak simpul yg digenerate 
level = 0
queue = []
visitedNode = []
path = []
costSolution = float('inf')

def searchBlankIndex(puzzle):
    for i in range(len(puzzle)):
        if puzzle[i] == BLANK: 
            return i 


def solvable(startPuzzle):
    return sigmaKurangPlusX(startPuzzle)%2==0


def sigmaKurangPlusX(startPuzzle):
    result = sum(kurangList)
    if searchBlankIndex(startPuzzle) in plusOneIndex:
        result+=1
    return result


def generateKurangList(startPuzzle):
    for index in range(len(startPuzzle)):
        value = startPuzzle[index]-1 #pada puzzle angkanya 1-16, pada array 0-15
        kurangList[value] = kurang(startPuzzle, index)
    printKurangList()


def kurang(startPuzzle, index):
    kurang = 0
    value = startPuzzle[index]
    for i in range(index+1, len(startPuzzle)):
        if startPuzzle[i] < startPuzzle[index]: kurang += 1
    return kurang


def printPuzzle(puzzle):
    fence = "---------------------------------"
    print(fence)
    for i in range(len(puzzle)):
        value = puzzle[i] if puzzle[i] != BLANK else " "
        print("  ", value, end="\t|") if (i%4 != 0 or i == 0) else print("\n" + fence + "\n  ", value, end="\t|")
    print("\n" + fence + "\n")


def printKurangList():
    print("=====Nilai fungsi Kurang(i)======"); print("\t i\tKurang(i)")
    print("---------------------------------")
    for index in range(len(kurangList)): 
        print("\t", index+1, "\t ", kurangList[index])


def cost(puzzle):
    g = 0
    for i in range(PUZZLE_SIZE):
        if final[i] != BLANK and puzzle[i] != final[i]: 
            g+=1
    return level + g


def popPuzzleQueue():
    global queue
    minIndex = searchMinCostElementQueue()
    item = queue[minIndex]
    del queue[minIndex]
    return item


def searchMinCostElementQueue():
    minCostIndex = 0
    for i in range(len(queue)):
        if queue[i][0] < queue[minCostIndex][0] or (queue[i][0] == queue[minCostIndex][0] and queue[i][2] > queue[minCostIndex][2]): # cost kurang dari atau cost sama tapi level kurang dari
            minCostIndex = i
    return minCostIndex


def solve(puzzle):
    global queue, visitedNode, countNode, costSolution, path
    tup = (cost(puzzle), puzzle, level)
    queue.append(tup)
    countNode = 1
    solution = queue[0][1]
    #print start puzzle
    print("Node ke-", countNode, "(PARENT NODE) <=> Cost: ", queue[0][0])
    printPuzzle(solution)
    while queue != [] and level < 20:
        solution = popPuzzleQueue()
        visitedNode.append(solution[1])
        if (solution[0] < costSolution):
            if (solution[2] < level):
                while (path[len(path)-1][2] >= solution[2]):
                    print("SSSSSSSSSSSSSSSSSS")
                    print(path[len(path)-1])
                    print("SSSSSSSSSSSSSSSSSS")
                    del path[len(path)-1]
            path.append(solution) 
            if (solution[1] == final):
                costSolution = solution[0]
            else:
                generateChildNode(solution[1])


def generateChildNode(puzzle):
    global level, queue, countNode
    generateNewLevel = True
    for direction in operator:
        if isPossibleSwap(puzzle, direction):
            childPuzzle = swapBlankPosition(puzzle, direction)
            if childPuzzle not in visitedNode:
                if generateNewLevel == True:
                    level+=1
                    generateNewLevel = False
                tup = (cost(childPuzzle), childPuzzle, level)
                queue.append(tup); countNode+=1
                print("Node ke-",countNode, "<=> Cost: ", cost(childPuzzle))
                printPuzzle(childPuzzle)
    print("Parent Node: ")
    printPuzzle(puzzle)
                

def swapBlankPosition(puzzle, direction):
    newPuzzle = copy.deepcopy(puzzle)
    indexBlank = searchBlankIndex(newPuzzle)
    if direction == "up":
        newPuzzle[indexBlank], newPuzzle[indexBlank-4] = newPuzzle[indexBlank-4], newPuzzle[indexBlank]
    elif direction == "down":
        newPuzzle[indexBlank], newPuzzle[indexBlank+4] = newPuzzle[indexBlank+4], newPuzzle[indexBlank]
    elif direction == "left":
        newPuzzle[indexBlank], newPuzzle[indexBlank-1] = newPuzzle[indexBlank-1], newPuzzle[indexBlank]
    else: #right
        newPuzzle[indexBlank], newPuzzle[indexBlank+1] = newPuzzle[indexBlank+1], newPuzzle[indexBlank]
    return newPuzzle


def isPossibleSwap(puzzle, direction):
    indexBlank = searchBlankIndex(puzzle)
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


puzzlepath = "./puzzle"
fileName = os.path.join(puzzlepath, input("File name: "))
# fileName = "3.txt"; fileName = os.path.join(puzzlepath, fileName)
file = open(fileName, "r")
start = [data for line in file for data in line.split()] #extract data from external file
start = list(map(lambda x: int(x) if x != "-" else BLANK, start)) #map to int list
print("=======Posisi awal Puzzle========"); 
printPuzzle(start)
print("=================================\n")
generateKurangList(start)
print("=================================\n")
print("Sigma Kurang(i) + X = ", sigmaKurangPlusX(start));  
if solvable(start):
    print("Karena", sigmaKurangPlusX(start), "% 2 == 0 maka puzzle : Solvable!\n")
    start_time = time.time()
    solve(start)
    runtime = time.time() - start_time


    print(queue)
    print("==========")
    print(visitedNode)
    print("==========")
    print(path)

    print("============Jalur B&B============"); i = 1
    for cost, node, level in path:
        print("Jalur ke-", i, "| Level: ", level, "| Cost: ", cost)
        printPuzzle(node); i+=1
    print("Runtime: %s seconds" %runtime)
    print("Jumlah simpul yang dibangkitkan:", countNode)
else:
    print("Karena", sigmaKurangPlusX(start), "% 2 != 0 maka puzzle : Not Solvable!")

file.close()