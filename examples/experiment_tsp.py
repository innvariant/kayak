import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mplpath
from scipy.spatial.distance import pdist, squareform

#Definition von Konstanten für die Anzeige der Stadtindizess
xshift=0.2
yshift=0.2

#Anzahl der Städte
cities = 20

#X- und Y- Koordinaten des Polygons, innerhalb dessen die Städte liegen
x = np.array([2, 10, 14, 11, 15, 14, 10, 7, 5, 2, 1, 3, 2])
y = np.array([2, 0, 2, 5, 9, 19, 16, 19, 16, 12, 6, 5, 2])
Verts = np.array([x,y]).transpose()
polygon = mplpath.Path(Verts)

#Erzeugen der Städte und der Plot der Städte in der grafischen Oberfläche
plt.figure(1)
plt.subplot(121)
plt.plot(x,y)
plt.grid(True)
#plt.hold(True)
i = 0
np.random.seed(seed=346466)
locations = np.zeros((cities,2)) #Zufällige Festlegung der Orte
while i in range(cities):
    xp = np.random.randint(0,max(x))
    yp = np.random.randint(0,max(y))
    isin = polygon.contains_point((xp, yp)) #testet ob der Punkt innerhalb des Polygons liegt
    print(xp , yp, isin)
    if isin:
        locations[i,:]=[xp,yp]
        plt.plot([xp],[yp],'ro')
        plt.text(xp+xshift,yp+yshift,str(i))
        i+=1
print(locations)
#Berechnung der euklidischen Distanz zwischen allen möglichen Stadtpaaren


class EuclideanFitness(object):
    def __init__(self, points):
        self._distances = squareform(pdist(points, 'euclidean'))
        self._number_points = len(points)
        self._costs = {}

    def cost(self, permutation):
        hash = ','.join(["%s"%el for el in permutation])
        if hash not in self._costs:
            cost = 0
            for city_ind in range(self._number_points - 1):
                x = int(permutation[city_ind])
                y = int(permutation[city_ind + 1])
                cost += self._distances[x, y]
            self._costs[hash] = cost
        return self._costs[hash]

fitness = EuclideanFitness(locations)


np.random.seed()
###########################################################################
#                      Genetischer Algorithmus zur Lösung des TSP         #
###########################################################################

print('-'*10 + '\nGA\n' + '-'*10)

#Definition der Konstanten für den GA
ITERATIONS = 5000
POPSIZE = 16
CROSSPROP = 0.99
MUTPROP = 0.05

bestDist=np.zeros(ITERATIONS) #In diesem Array wird für jede Iteration die beste Distanz gespeichert
#Erzeugen einer zufälligen Startpopulation
population=np.zeros((POPSIZE,cities+1))
for j in range(POPSIZE):
        population[j,0:cities] = np.random.permutation(cities)
        population[j,cities] = population[j,0]
print(population)

for permut in population:
    cost = fitness.cost(permut)
    print('%s := %.2f' % (permut, cost))

plt.show()