board = [
        [-1, 5, 5, -1, 5, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, 7, 3, -1, 5, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, 4, 1, -1, 5, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, 2, 8, -1, 5, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, 7, 3, -1, 5, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    ]
tiles = [5, 5, 5, 5, 5]
bestMove = (-1, [])

def horizontalTotal(i, j, val, newBoard):
    n, m = i, j
    currSum = val
    length = 1
    while m-1 >= 0 and newBoard[n][m-1] != -1:
        currSum += newBoard[n][m-1]
        m-=1
        length += 1
    n, m = i, j
    while m+1 < len(newBoard[n]) and newBoard[n][m+1] != -1:
        currSum += newBoard[n][m+1]
        m+=1
        length += 1
    return currSum, length


def verticalTotal(i, j, val, newBoard):
    n, m, = i, j
    currSum = val
    length = 1
    while n-1 >= 0 and newBoard[n-1][m] != -1:
        currSum += newBoard[n-1][m]
        n-=1
        length += 1
    n, m = i, j
    while n+1 < len(newBoard) and newBoard[n+1][j] != -1:
        currSum += newBoard[n+1][m]
        n+=1
        length += 1
    
    return currSum, length


def valid(tilesUsed, horizontal):
    newBoard = [[board[i][j] for j in range(len(board[i]))] for i in range(len(board))]
    for tile in tilesUsed:
        newBoard[tile[0]][tile[1]] = tile[2]
    otherTotal = 0
    directionTotal = 0
    if horizontal:
        directionTotal, length = horizontalTotal(tilesUsed[0][0], tilesUsed[0][1], tilesUsed[0][2], newBoard)
        if length > 5:
            return False, 0
        if length > 1:
            if directionTotal % 5 != 0:
                return False, 0
        else:
            directionTotal = 0
        for tile in tilesUsed:
            tempTotal, length = verticalTotal(tile[0], tile[1], tile[2], newBoard)
            if length > 5:
                return False, 0
            if length > 1:
                if tempTotal % 5 != 0:
                    return False, 0
                otherTotal += tempTotal
    else:
        directionTotal, length = verticalTotal(tilesUsed[0][0], tilesUsed[0][1], tilesUsed[0][2], newBoard)
        if length > 5:
                return False, 0
        if length > 1:
            if directionTotal % 5 != 0:
                return False, 0
        else:
            directionTotal = 0
        for tile in tilesUsed:
            tempTotal, length = horizontalTotal(tile[0], tile[1], tile[2], newBoard)
            if length > 5:
                return False, 0
            if length > 1:
                if tempTotal % 5 != 0:
                    return False, 0
                otherTotal += tempTotal
    
    return True, otherTotal + directionTotal


def backtrackVertical(i, j, tileCount, tilesUsed, used, seen):
    global board, tiles
    global bestMove
    if tileCount > 0:
        allowed, total = valid(tilesUsed, False)
        if allowed:
            if bestMove[0] < total:
                bestMove = (total, list(tilesUsed))

    if tileCount == 5:
        return
    seen[i][j] = True
    if i+1 < len(board):
        if not seen[i+1][j]:
            if board[i+1][j] != -1:
                backtrackVertical(i+1, j, tileCount+1, tilesUsed, used, seen)
            else:
                for k in range(5):
                    if not used[k]:
                        used[k] = True
                        tilesUsed.append((i+1, j, tiles[k]))
                        backtrackVertical(i+1, j, tileCount+1, tilesUsed, used, seen)
                        tilesUsed.pop()
                        used[k] = False
    
    if i-1 >= 0:
        if not seen[i-1][j]:
            if board[i-1][j] != -1:
                backtrackVertical(i-1, j, tileCount+1, tilesUsed, used, seen)
            else:
                for k in range(5):
                    if not used[k]:
                        used[k] = True
                        tilesUsed.append((i-1, j, tiles[k]))
                        backtrackVertical(i-1, j, tileCount+1, tilesUsed, used, seen)
                        tilesUsed.pop()
                        used[k] = False
    seen[i][j] = False


def backtrackHorizontal(i, j, tileCount, tilesUsed, used, seen):
    global board, tiles
    global bestMove
    if tileCount > 0:
        allowed, total = valid(tilesUsed, True)
        if allowed:
            if bestMove[0] < total:
                bestMove = (total, list(tilesUsed))
    
    if tileCount == 5:
        return
    seen[i][j] = True
    if j+1 < len(board[i]):
        if not seen[i][j+1]:
            if board[i][j+1] != -1:
                backtrackHorizontal(i, j+1, tileCount+1, tilesUsed, used, seen)
            else:
                for k in range(5):
                    if not used[k]:
                        used[k] = True
                        tilesUsed.append((i, j+1, tiles[k]))
                        backtrackHorizontal(i, j+1, tileCount+1, tilesUsed, used, seen)
                        tilesUsed.pop()
                        used[k] = False
    
    if j-1 >= 0:
        if not seen[i][j-1]:
            if board[i][j-1] != -1:
                backtrackHorizontal(i, j-1, tileCount+1, tilesUsed, used, seen)
            else:
                for k in range(5):
                    if not used[k]:
                        used[k] = True
                        tilesUsed.append((i, j-1, tiles[k]))
                        backtrackHorizontal(i, j-1, tileCount+1, tilesUsed, used, seen)
                        tilesUsed.pop()
                        used[k] = False
    seen[i][j] = False


def placeableSpace(i, j):
    if board[i][j] != -1:
        return False
    if i+1 < len(board) and board[i+1][j] != -1:
        return True
    if i-1 >= 0 and board[i-1][j] != -1:
        return True
    if j+1 < len(board[i]) and board[i][j+1] != -1:
        return True
    if j-1 >= 0 and board[i][j-1] != -1:
        return True
    
    return False


def main():
    #Find perimeter tiles
    for i in range(len(board)):
        for j in range(len(board[i])):
            if placeableSpace(i, j):
                for k in range(5):
                    tilesUsed = [(i, j, tiles[k])]
                    used = [False for _ in range(5)]
                    used[k] = True
                    seen = [[False]*len(board[i]) for i in range(len(board))]
                    backtrackHorizontal(i, j, 1, tilesUsed, used, seen)
                    backtrackVertical(i, j, 1, tilesUsed, used, seen)
    
    print('BEST MOVE:', bestMove)
                


if __name__ == '__main__':
    main()    
        
