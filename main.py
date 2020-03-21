BLANK = 16
PUZZLE_SIZE = 16
ROW_SIZE = 4
plusOneIndex = [1, 3, 4, 6, 8, 11, 12, 14] #digunakan untuk X = 1 pada Solvable(puzzle)
kurangList = [0 for i in range(PUZZLE_SIZE)]

def blankIndex(puzzle):
    for i in range(len(puzzle)):
        if puzzle[i] == BLANK: 
            return i 

def solvable(puzzle):
    return sigmaKurangPlusX(puzzle)%2==0

def sigmaKurangPlusX(puzzle):
    result = sum(kurangList)
    if blankIndex(puzzle) in plusOneIndex:
        result+=1
    return result

def generateKurangList(puzzle):
    for index in range(len(puzzle)):
        value = puzzle[index]-1
        kurangList[value] = kurang(puzzle, index)
    printKurangList()

def kurang(puzzle, index):
    kurang = 0
    value = puzzle[index]
    for i in range(index+1, len(puzzle)):
        if puzzle[i] < puzzle[index]: kurang += 1
    return kurang

def printPuzzle(puzzle):
    for i in range(len(puzzle)):
        value = puzzle[i] if puzzle[i] != BLANK else " "
        print("", value, end="\t") if (i%4 != 0 or i == 0) else print("\n", value, end="\t")
    print()

def printKurangList():
    print("===Nilai fungsi Kurang(i)==="); print("i\tKurang(i)")
    for index in range(len(kurangList)): 
        print(index+1, "\t", kurangList[index])

# fileName = input("File name: ")
fileName = "puzzle.txt"
file = open(fileName, "r")
start = [data for line in file for data in line.split()]
start = list(map(lambda x: int(x) if x != "-" else BLANK, start))
print("=====Posisi awal Puzzle====="); 
printPuzzle(start)
print("============================\n")
generateKurangList(start)
print("============================\n")
print("Sigma Kurang(i) + X = ", sigmaKurangPlusX(start), "\n");  
if solvable(start):
    print("Solvable!")
    
else:
    print("Not Solvable!")
