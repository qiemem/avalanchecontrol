from pylab import *

#def stabilize(sandpile):
#    rows, cols = sandpile.shape
#    sandpile = array(sandpile)
#    topplings = 0
#    unstables = True
#    #while any(sandpile[1:rows-1, 1:cols-1]>3):
#    while unstables:
#        unstables = False
#        for i in xrange(1, rows-1):
#            for j in xrange(1, cols-1):
#                if sandpile[i,j] > 3:
#                    sandpile[i,j] -= 4
#                    sandpile[i+1, j] += 1
#                    sandpile[i-1, j] += 1
#                    sandpile[i, j+1] += 1
#                    sandpile[i, j-1] += 1
#                    topplings += 1
#                    unstables = True
#    return sandpile, topplings

def iter_sandpile(sandpile, strategy = None):
    sandpile = array(sandpile)
    rows, cols = sandpile.shape
    while True:
        if strategy is not None:
            sandpile = strategy(sandpile)
        r = randint(rows)
        c = randint(cols)
        sandpile[r,c]+=1
        sandpile, firings = stabilize(sandpile)
        yield sandpile, firings
        
def stabilize(sandpile):
    rows, cols = sandpile.shape
    withsinks = zeros((rows+2, cols+2))
    withsinks[1:rows+1, 1:cols+1] = sandpile
    firings = zeros(sandpile.shape)
    topplings = 0
    unstables = True
    #while any(sandpile[1:rows-1, 1:cols-1]>3):
    while unstables:
        unstables = False
        for i in xrange(1, rows+1):
            for j in xrange(1, cols+1):
                if withsinks[i,j] > 3:
                    withsinks[i,j] -= 4
                    withsinks[i+1, j] += 1
                    withsinks[i-1, j] += 1
                    withsinks[i, j+1] += 1
                    withsinks[i, j-1] += 1
                    firings[i-1,j-1] += 1
                    unstables = True
    return withsinks[1:rows+1, 1:cols+1], firings

def index_map(func, mx):
    rows = mx.shape[0]
    cols = mx.shape[1]
    return array([[func(i, j) for j in range(cols)] for i in range(rows)])

def grain_map(func, sandpile):
    def grain_func(i, j):
        sandpile[i,j] += 1
        result = func(i, j)
        sandpile[i,j] -= 1
        return result
    return index_map(grain_func, sandpile)

def avalanche_matrix(sandpile):
    return grain_map(lambda i,j : stabilize(sandpile)[1], sandpile)

def potential_energy(sandpile):
    return avalanche_matrix(sandpile).sum()

def potential_matrix(sandpile):
    return grain_map(lambda i,j : potential_energy(stabilize(sandpile)[0]), sandpile)

def worst_case(sandpile):
    return avalanche_matrix(sandpile).sum(3).sum(2).max()

def worst_case_matrix(sandpile):
    return grain_map( lambda i,j : worst_case(stabilize(sandpile)[0]), sandpile)

def volatility_matrix(avalanches):
    return index_map(lambda i,j: (avalanches[:,:,i,j] != 0).sum(), avalanches)

def rand_sandpile(rows, cols):
    return stabilize(randint(0, 9, (rows, cols)))[0]

def show_mat(mat, **kwargs):
    def onpick(event):
        row = round(event.mouseevent.ydata)
        col = round(event.mouseevent.xdata)
        print(str(mat[row, col]))
    figure()
    im=imshow(mat, interpolation='none', **kwargs)
    colorbar()
    im.figure.canvas.mpl_connect('pick_event', onpick)
    return im

def show_sandpile(mat):
    rows, cols = mat.shape
    im = show_mat(mat, picker=True)
    im.row = im.col = None
    def onpick(event):
        print('Showing sandpile')
        row = round(event.mouseevent.ydata)
        col = round(event.mouseevent.xdata)
        if row == im.row and col == im.col:
            im.set_array(mat)
            show()
            im.row = im.col = None
        else:
            print('Showing avalanche', row, col)
            mat[row, col]+=1
            _, aval = stabilize(mat)
            mat[row,col]-=1
            print('Sand: {}, Firings: {}, Radius: {}'.format(
                mat[row, col], aval.sum(), (aval!=0).sum()))
            im.set_array(aval)
            show()
            im.row, im.col = row, col
    im.figure.canvas.mpl_connect('pick_event', onpick)
    return im

def minmax(sandpile, depth = 2):
    rows, cols = sandpile.shape
    def minimize(s, row, col, depth):
        s[row, col] += 1
        next_s,firings = stabilize(s)
        base = (firings!=0).sum()
        s[row, col] -= 1
        if depth == 1:
            return base
        else:
            return array([maximize(next_s, r, c, depth-1) for r in range(rows) for c in range(cols)]).min() + base


    def maximize(s, row, col, depth):
        s[row, col] += 1
        next_s,firings = stabilize(s)
        base = (firings!=0).sum()
        s[row, col] -= 1
        if depth == 1:
            return base
        else:
            return array([minimize(next_s, r, c, depth-1) for r in range(rows) for c in range(cols)]).max() + base
    min_score = inf
    minr, minc = -1,-1
    for row in range(rows):
        for col in range(cols):
            s = maximize(sandpile, row, col, depth)
            if s < min_score:
                min_score = s
                minr, minc = row, col
    sandpile[minr, minc] +=1
    return sandpile

    
