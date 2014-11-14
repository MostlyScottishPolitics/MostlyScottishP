import mdp
import numpy
import matplotlib.pyplot as plt
import pylab
import os.path
import psycopg2

#Load up the giant 5724x129 null matrix (matrix with only zeroes)
X = numpy.genfromtxt("Null.csv",delimiter=",")

#Merge loaded data with the null matrix
with open('C:\Users\Kris\Desktop\Temp Sirogers Data\pca\pca\\\\votes7.csv') as f:
    for line in f:
        thisLine = line.split(",")
        try:
            msp = int(thisLine[1])
            div = int(thisLine[2])
            X[msp][div] = int(thisLine[3])
            print X[msp][div]
        except:
            print "Value was broken here"

#Output to csv with each unit being a float
X = X.astype(float)
numpy.savetxt("OuputText.csv", X, fmt="%s", delimiter=",")
print "data Saved to Output"
print 

#Set output dimensions, and load up text
imdp = mdp.nodes.PCANode(output_dim=2)
print "loading file up again"
data = numpy.loadtxt(open("OuputText.csv", 'rb'), dtype='float', delimiter=',', usecols=range(1,129))

#Process matrix using PCA
matrix = imdp(data)
print ""
print "Output Matrix"
print matrix

#Save to file
numpy.savetxt("OuputMatrix.csv", matrix, fmt="%s", delimiter=",")

#Plot graph
cm = plt.cm.get_cmap('RdYlBu')
z = matrix
fig = plt.figure()
ax = fig.add_subplot(111)

ax.scatter(matrix[:,0], matrix[:,1], c='r', marker='o')
plt.show()
