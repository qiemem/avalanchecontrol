from pylab import *
from sandpiles import *

rows, cols = 15,15
s = rand_sandpile(rows, cols)
a = avalanche_matrix(s)
f = a.sum(3).sum(2) # matrix of number of firings from adding a grain at each spot
r = (a!=0).sum(3).sum(2) # matrix of number of vertices firest
v = volatility_matrix(a)

e = zeros((rows, cols))
for i in xrange(rows):
    for j in xrange(cols):
        e[i,j] = sum(multiply((a[i,j] != 0), v))

show_sandpile(s)
show_mat(f)
show_mat(r)
show_mat(e)
show_mat(v)

p = potential_matrix(s) # TAKES A LONG TIME!

w = worst_case_matrix(s) # TAKES A LONG TIME!

show_mat(p)
figure(); scatter(f.flatten(), p.flatten()) # num firings vs resulting potential
figure(); scatter(r.flatten(), p.flatten()) # radius vs resulting potential
