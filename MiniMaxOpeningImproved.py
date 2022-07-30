import sys

"""
    Input: A board Position
    Output: Static estimation for the current board Position. (Integer)
"""

class Node:
    def __init__(self, boardPos, depth):
        self.position = boardPos
        self.depth = depth
    
class MiniMax:
    def __init__(self, depth):
        self.countStaticEstimation = 0
        self.maxDepth = depth
        self.gmo = GenerateMovesOpening()
        self.maxPos = ""

    def maxMin(self, n : Node):
        #Generate for white
        if n.depth == self.maxDepth:
            return self.staticEstimation(n.position)
        moves = self.gmo.generate(n.position)
        #print(f"level : {n.depth}\tpos : {currPos}\tmoves: {moves}")
        currMax = float("-inf")
        for move in moves:
            childVal = self.minMax(Node(move, n.depth + 1))
            #print(f"level : {n.depth}\tpos : {nextPos}\tval : {childVal}")
            if childVal > currMax:
                currMax = childVal
                if n.depth == 0 : 
                    self.maxPos = move
        return currMax
    
    def minMax(self, n : Node):
        #Generate for black
        if n.depth == self.maxDepth:
            return self.staticEstimation(n.position)
        currPos = self.gmo.reversePosition(n.position)
        currMin = float("inf")
        moves = self.gmo.generate(currPos)
        for move in moves:
            childVal = self.maxMin(Node(self.gmo.reversePosition(move), n.depth + 1))
            currMin = min(currMin, childVal)
        return currMin
        
    
    
    def staticEstimation(self, boardPos : str)->int:
        self.countStaticEstimation += 1
        numWhitePieces, numBlackPieces = 0, 0
        for pos in boardPos:
            if pos == 'W':
                numWhitePieces += 1
            elif pos == 'B':
                numBlackPieces += 1
        
        whiteMill, blackMill = self.gmo.getNumCloseMills(boardPos)
        whiteAdvCount, blackAdvCount = self.gmo.getNumAdvantagePosition(boardPos)

        return (2 * numWhitePieces + 5 * whiteMill + whiteAdvCount - (2 * numBlackPieces + 5 * blackMill + blackAdvCount))
    

class GenerateMovesOpening:
    """
    Input: A board Position
    Output: A list of board Positions.
    """
    def __init__(self):
        self.res = []
        self.millPos = {0 : [[2,4], [6,18]], 1 : [[3,5], [11,20]], \
                    2:[[0,4], [7,15]], 3 : [[1,5],[10,17]], 4 : [[0,2], [8,12]],\
                     5 : [[1,3], [9,14]] ,  6 : [[0, 18], [7,8]],\
                    7 :[[2, 15], [6,8]], 8 :[[4,12], [6,7]], \
                    9 :[[5,14], [10, 11]], 10: [[3, 17], [9, 11]],\
                    11 :[[1, 20], [9, 10]], 12:[[4,8], [13, 14], [15, 18]],\
                    13:[[12, 14], [16, 19]], 14:[[5,9], [12, 13], [17, 20]],\
                    15 :[[2, 7], [12, 18], [16, 17]], 16:[[13, 19], [15, 17]], \
                    17: [[3, 10], [14, 20], [15, 16]], 18 : [[0,6], [12, 15], [19, 20]],\
                    19: [[13, 16], [18, 20]], 20:[[1, 11], [14, 17], [18, 19]]}
        
    
    def generate(self, currBoardPos):
        self.res = []
        self.generateAdd(currBoardPos)
        return self.res

    def reversePosition(self, pos):
        newPos = ""
        for ch in pos:
            
            if ch == 'W':
                newPos += 'B'
            elif ch == 'B':
                newPos += 'W'
            else:
                newPos += ch
        return newPos
    """
    Input: A board Position
    Output: A list of board Positions.
    """
    def generateAdd(self, currBoardPos : str):
        for idx, pos in enumerate(currBoardPos):
            if pos == 'x':
                newBoardPos = currBoardPos[:idx]+'W'+currBoardPos[idx+1:]
                if self.closeMill(idx, newBoardPos):
                    self.generateRemove(newBoardPos)
                else:
                    self.res.append(newBoardPos)
        
    
    def closeMill(self, currLoc : int, boardPos: str)->bool:
        if boardPos[currLoc] == 'x':
            return False
        
        for pos1, pos2 in self.millPos[currLoc]:
            if boardPos[pos1] == boardPos[pos2] == boardPos[currLoc]:
                return True

        return False
    
    def getNumCloseMills(self, boardPos : str)->int:
        numBlackCloseMills, numWhiteCloseMills = 0, 0
        for idx in range(len(boardPos)):
            for pos1, pos2 in self.millPos[idx]:
                if boardPos[idx] == 'B' == boardPos[pos1] == boardPos[pos2]:
                    numBlackCloseMills += 1
                elif boardPos[idx] == 'W' == boardPos[pos1] == boardPos[pos2]:
                    numWhiteCloseMills += 1
        return (numWhiteCloseMills // 3, numBlackCloseMills // 3)

    def getNumAdvantagePosition(self, boardPos : str):
        advantagePositions = set([12, 14, 15,17, 18, 20])
        advantageCount = disadvantageCount = 0
        for idx, pos in enumerate(boardPos):
            if pos == 'W' and idx in advantagePositions:
                advantageCount += 1
            elif pos == 'B' and idx in advantagePositions:
                disadvantageCount += 1
        return (advantageCount, disadvantageCount)   
    
    def generateRemove(self, boardPos : str)-> None:
        for idx, pos in enumerate(boardPos):
            if pos == 'B':
                if not self.closeMill(idx, boardPos):
                    self.res.append(boardPos[:idx]+'x'+boardPos[idx+1:])


if __name__=='__main__':
    lenArgs = len(sys.argv)
    opts = sys.argv

    if lenArgs != 4:
        print("!!!Here is what is expected : \npython <python_file_to_execute> <inputFile.txt> <outputFile.txt> <depth>\n")
        sys.exit(2)

    inputFile, outputFile, depth = opts[1], opts[2], int(opts[3])
    currBoardPos = ''
    with open(inputFile, 'r') as f:
        currBoardPos = f.readline()
    if (len(currBoardPos) != 21):
        print("Error : Please check the length of the board Position entered.")
        sys.exit(2)
    
    #main Program call

    minimax = MiniMax(depth)
    root = Node(currBoardPos, 0)
    minimaxEstimation = minimax.maxMin(root)
    bestPos = minimax.maxPos

    #Writing output of Best Position evaluated to file.
    with open(outputFile, 'w') as out:
        out.write(bestPos)
    print("**************************************************")
    print(f"Input : {currBoardPos}")
    print(f"Depth : {depth}")
    print("------------ IMPROVED MINIMAX OPENING ------------")
    print(f"Board Position: {bestPos}")
    print(f"Positions evaluated by static estimation: {minimax.countStaticEstimation}")
    print(f"MINIMAX estimate: {minimaxEstimation}")
    print("**************************************************")
