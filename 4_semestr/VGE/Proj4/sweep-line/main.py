import sys

import matplotlib.pyplot as plt
from Colorizer import *
from DCELfile import *
from monotonepart import *
from triangulatemono import *
DEBUG = False

n = int(sys.argv[1])
from numpy.random import randint
from numpy import lexsort,asarray,append
coords = randint(0,90000, size=(2,n))
x = coords[0] 
y = coords[1]
ind = lexsort((y,x))
coords = [(x[i],y[i]) for i in ind] 
x = asarray([c[0] for c in coords])
y = asarray([c[1] for c in coords])
pivot = coords[0]

y_diff_pivot = y-pivot[1]
x_diff_pivot = x-pivot[0]
tan = (y_diff_pivot[1:]+0.0)/x_diff_pivot[1:]

pairs = zip(tan,coords[1:])
pairs = sorted(pairs, key = lambda (x,y): x)

coords = asarray([pivot])
coords = append(coords, asarray( zip(*pairs)[-1] ), axis=0 )
coords = append(coords, asarray([pivot]), axis=0 )

p=[(c[1],c[0]) for c in coords][::-1][1:]
print 'Polygon', p
d = buildSimplePolygon(p)
map_points ={x.coords:x for x in d.getVertices()}
for i in range(1,len(p)-1):
    map_points[p[i]].next = map_points[p[i+1]]
    map_points[p[i+1]].prev = map_points[p[i]]
map_points[p[0]].prev = map_points[p[-1]]
map_points[p[0]].next = map_points[p[1]]
map_points[p[1]].prev = map_points[p[0]]
map_points[p[-1]].next = map_points[p[0]]

d1 = d
def newline(p, q):
    X = np.linspace(p[0], q[0],endpoint=True)
    Y = np.linspace(p[1],q[1],endpoint=True)
    return X,Y

def nowDraw(toDraw, verbose=False):
    if verbose:
        for x in toDraw:
            plt.plot(x[0],x[1],x[2])
        plt.show()

toDraw = []
for e in d.getEdges():
    p1,q1 = list(e.origin.coords),list(e.getTwin().origin.coords)
    X,Y = newline(p1,q1)
    toDraw.append([X,Y,'r'])

nowDraw(toDraw)
DEBUG = False
ret = getTrapEdges(d)
for r in ret:
    print 'TrapEdges', r.left, r.right
    X,Y = newline(r.left,r.right)
    toDraw.append([X,Y,'b'])
    toDraw.append([r.pivot.coords[0],r.pivot.coords[1],'go'])

nowDraw(toDraw)
DEBUG = False
diagnls = monotonePartitioningDgnls(d)
for dg in  diagnls:
    print 'Partition', dg[0].coords, dg[1].coords
    X,Y = newline(dg[0].coords,dg[1].coords)
    toDraw.append([X,Y,'g'])

nowDraw(toDraw)
listOfMonos = insertDgnls(d,[(x[0].coords,x[1].coords) for x in diagnls])
import os
def createMonoPolygon(d,p):
    f = open('cgalinput','w')
    f.write(str(len(p))+"\n")
    for c in p:
        f.write(str(c[0])+" "+str(c[1])+" ")
    f.close()
    os.system("g++ makemonotone.cpp -lCGAL -lgmp")
    os.system("./a.out > cgalout")
    with open('cgalout','r') as f:
        content = f.readlines()
    content = [x.strip() for x in content] 
    result = []

    for c in content:
        c = c.split(' ')
        n = c[0]
        j = 1
        p = []
        for i in range(int(n)):
            p.append((float(c[j]),float(c[j+1])))
            j += 2
        d = buildSimplePolygon(p)
        map_points ={x.coords:x for x in d.getVertices()}
        for i in range(1,len(p)-1):
            map_points[p[i]].next = map_points[p[i+1]]
            map_points[p[i+1]].prev = map_points[p[i]]
        map_points[p[0]].prev = map_points[p[-1]]
        map_points[p[0]].next = map_points[p[1]]
        map_points[p[1]].prev = map_points[p[0]]
        map_points[p[-1]].next = map_points[p[0]]
        result.append(d)
    return result

listOfMonos = createMonoPolygon(d,p)

toDraw = []
for m in listOfMonos:
    for e in m.getEdges():
        p1,q1 = list(e.origin.coords),list(e.getTwin().origin.coords)
        X,Y = newline(p1,q1)
        toDraw.append([X,Y,''])
        toDraw.append([e.origin.coords[0],e.origin.coords[1],'o'])

nowDraw(toDraw)

DEBUG = False
toDraw = []
listOfTriangles = []
tmp = -1

for mono in listOfMonos:
    diagnls = triangulateMonotonePolygon(mono)
    vv = [(x[0].coords,x[1].coords) for x in diagnls]
    listOfTriangles += insertDgnls(mono,vv)
    tmp+=len(diagnls)+1

listOfTriangles = [[t.getFaces()[1].getOuterBoundary()[0].origin,
                    t.getFaces()[1].getOuterBoundary()[1].origin,
                    t.getFaces()[1].getOuterBoundary()[2].origin
                   ] for t in listOfTriangles]

for t in listOfTriangles:
    p1,q1 = list(t[0].coords),list(t[1].coords)
    print 'listOfTriangles0',p1,q1
    X,Y = newline(p1,q1)
    toDraw.append([X,Y,'r'])
    p1,q1 = list(t[1].coords),list(t[2].coords)
    print 'listOfTriangles1',p1,q1
    X,Y = newline(p1,q1)
    toDraw.append([X,Y,'b'])
    p1,q1 = list(t[2].coords),list(t[0].coords)
    print 'listOfTriangles2', p1, q1
    X,Y = newline(p1,q1)
    toDraw.append([X,Y,'g'])


nowDraw(toDraw)

colorizer = Colorizer(d,listOfTriangles)
x = colorizer.colorize()

toDraw = []
for e in d1.getEdges():
    p1,q1 = list(e.origin.coords),list(e.getTwin().origin.coords)
    X,Y = newline(p1,q1)
    toDraw.append([X,Y,'r'])
for g in x[0]:
    toDraw.append([g.coords[0],g.coords[1],'bo'])
plt.plot(0,0, label='Gaurds required: '+str(x[1]))
plt.legend()
nowDraw(toDraw)
os.system('rm cgalinput cgalout a.out')
