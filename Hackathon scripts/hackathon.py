# Read the matrix
# no new line char after reading
# make sure each char is read as (int)
# seems we should put -1 for unavailable cell

#HINTS TO PROVIDE
# Min Max Algo (a day before)
# Alpha Beta Pruning Algo (a day before)
# Probably give tic tac toe as sample (during 1st half)
# counter to max iteratiosn row x col  (for AI) not to stuck in faulty recursion (tip)
import sys
matrix = []
input_file = '/usr/pic1/Input_matrix.txt'
row = 0
current_pos = []
matrix_score = []

def getMatixFromArgs():
    global row
    board_line = sys.argv[2]
    count = 0
    for i in board_line:        
        if count == 0:
            row1 = []
        row1.append(i)
        count += 1
        if count == 7:
            matrix.append(row1)
            matrix_score.append([0 for x in range(7)])
            count = 0
    row = 7            

def getMatrix():
    global row
    with open(input_file, 'r') as file:
        for line in file:
            #print line
            #print type(line)
            line = line.rstrip('\n')
            matrix.append([int(char) for char in line.split(',')])
            matrix_score.append([0 for x in range(7)])
            row = row + 1
    row = row - 1  #last row is player_id Turn
    #print '---final', row

def findPlayer(player_id):
    col = -1    
    for r in range(row):
        current_row = matrix[r]
        #print current_row        
        try:
            col = current_row.index(player_id)
            #print 'Yest', col
            return r, col
        except ValueError:
            #print 'Invlaie'
            pass
    return (-1,-1) #FAIL
    #print '---colr --', col

def findAvailable(player_pos):
    cr,cc = player_pos
    rs = cr - 1
    cs = cc - 1
    re = cr + 1
    ce = cc + 1
    #print rs,re, cs , ce
    max = -1
    max_x = -1
    max_y = -1
    for r in range(rs,re+1):
        for c in range(cs, ce+1):
            if r < row and c < row and r >= 0 and c >= 0 and ( matrix[r][c] != 'O' and matrix[r][c]!='X') :
                #print 'checking', r,c
                if matrix[r][c] == 'O':
                        pass
                #print matrix_score[r][c], type(matrix_score[r][c])
                if max < matrix_score[r][c]:
                    max = matrix_score[r][c]
                    max_x, max_y = r,c
                #print max

    return (max_x,max_y)

#def doesMoveWin(pos_x, pos_y):
    #Does this move causes other player to loose?
    # Eliminate if outside other player -1 =1
    

def evaluateScoreMatrix():
    for r in range(row):
        for c in range(row):
            generateScore(r,c)

def generateScore(pos_x, pos_y):
    # This should ideally be player id based
    # We should store the score in matrix as a tuple like: ms[r][c] = (score_id0,score_id1)
    cr,cc = pos_x, pos_y
    rs = cr - 1
    cs = cc - 1
    re = cr + 1
    ce = cc + 1
    score = 0
    if matrix[pos_x][pos_y] == 'O' or matrix[pos_x][pos_y] == 'X' or matrix[pos_x][pos_y] == 'b':
        try:
            matrix_score[pos_x][pos_y] = -1
        except IndexError,e:
            pass
        return

    for r in range(rs,re+1):
        for c in range(cs, ce+1):
            if r < row and c < row and r >= 0 and c >= 0 :
                if len(matrix_score[r]) == 0:
                    #initialise row with [0] value
                    matrix_score[r].append([0])
                #Important exlcude pos_x and pos_y (its own position)
                if matrix[r][c] == '-' and (r,c) !=(pos_x, pos_y):
                    score += 1
    try:
        matrix_score[pos_x][pos_y] = score
    except IndexError, e:
        pass

    
#def scoreMatrix(player_id):
    
    
def generateBlockPose(player_id):
    """
    As of now this will get the most preferred position for the other player
    and block that
    """
    return generateNewPos(getNextTurn(player_id))    
def generateNewPos(player_id):
    player_pos = current_pos[player_id - 1]
    new_pos = findAvailable(player_pos)
    if new_pos == (-1,-1):
        #print "No position Available"
        return (-1,-1)
    return new_pos
    
def updateInputFile():
    with open(input_file, 'w') as file:
        for row in matrix:
            #print line
            #print type(line)
            line = [ str(x) for x in row]
            line = ','.join(line)
            line = '%s\n'%line
            file.write(line)

def printMatrix(matrix):
    from prettytable import PrettyTable
    t = PrettyTable([0,1,2,3,4,5,6])
    #print '----> ', row
    for r in range(row):
        t.add_row(matrix[r])
    #print t

def getTurn():
    return matrix[-1][0]

def getNextTurn(id):
    """
    f(id) = 3 - id
    """
    return 3-int(id)




##### Game Starts #######

getMatixFromArgs()
#printMatrix(matrix)
evaluateScoreMatrix()
#printMatrix(matrix_score)
turn = sys.argv[1]
current_pos.append(findPlayer('O'))
current_pos.append(findPlayer('X'))
#print current_pos
if turn == 'O':
    player_id = 1
else:
    player_id = 2
new_pos = generateNewPos(player_id)
block_pos = generateBlockPose(player_id)
x = [new_pos[0], new_pos[1], block_pos[0], block_pos[1]]
print '%s,%s,%s,%s' %(new_pos[0], new_pos[1], block_pos[0], block_pos[1])
#print new_pos[0],',', new_pos[1],',', block_pos[0],',', block_pos[1]
#sys.stderr.write('%s,%s' %(new_pos[0],new_pos[1]))
#sys.stderr.write('%s,%s' %(block_pos[0], block_pos[1]))

"""
getMatrix()
#print matrix
current_pos.append(findPlayer(1))
current_pos.append(findPlayer(2))
print current_pos
win = False
turn = getTurn()
count = 0

while (not win):
    print "Turn for player %s" %turn
    print "Board:"
    printMatrix(matrix)
    print "Score Board:"
    evaluateScoreMatrix()
    printMatrix(matrix_score)
    print "Ready to move player %s" %turn
    new_pos = generateNewPos(turn)
    block_pos = generateBlockPose(turn) 
    if new_pos == (-1,-1):
        win = True        
    else:
        cr, cc = current_pos[turn-1]
        nr, nc = new_pos
        br, bc = block_pos
        matrix[cr][cc] = -1
        matrix[nr][nc] = turn
        matrix[br][bc] = -1 #Block pos
        current_pos[turn-1] = new_pos
        print 'Moving player %s to %s %s' %(turn, nr, nc)
        matrix[-1] = [getNextTurn(turn)]
        updateInputFile()
    turn = getNextTurn(turn)

    count += 1
if win:
        print 'Player %s won'%turn
        print 'Total moves: %s' %count
"""