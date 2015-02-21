import numpy as np
import random
from collections import Counter
from random import randint

# random.seed(100)

class Node(object):

	 def __init__(self, data, label):
		self.data = data
		self.orig_label = label
		self.cluster = 0

	 def __str__(self):
		return "data=%s, label=%s" % (self.data, self.orig_label)

class DataSet(object):

	def __init__(self, data_file, label_file):
		self.nodes = []
		data = open(data_file, 'r').read().split("\n")
		labels = open(label_file, 'r').read().split("\n")

		for i in range(len(data)):
			vector = np.fromstring(data[i], dtype=int, sep=" ")
			self.nodes.append(Node(vector, labels[i]))

	def getNumFeatures(self):
		return len(self.nodes)


def kmeans(dataSet, k, debug):
	
	# Initialize centroids randomly
	numFeatures = dataSet.getNumFeatures()
	centroids = getRandomCentroids(dataSet.nodes,numFeatures, k)
	vector_size = 784

	# Initialize book keeping vars.
	iterations = 0
	oldCentroids = np.zeros((k, vector_size))
	labels = []

	# Run the main k-means algorithm
	while not shouldStop(oldCentroids, centroids, iterations):
		# Save old centroids for convergence test. Book keeping.
		oldCentroids = centroids
		iterations += 1
		
		# Assign labels to each datapoint based on centroids
		labels = []
		cluster_sums = np.zeros((k, vector_size))
		new_centroids = np.zeros((k, vector_size))

		cluster_sizes = [1] * k
		for node in dataSet.nodes:
			closest = 0
			distance = dist(node.data, centroids[0])
			for i in range(len(centroids)):
				temp = dist(node.data, centroids[i])
				if(temp < distance):
				  closest = i
				  distance = temp
			# print node.orig_label
			cluster_sums[closest] = cluster_sums[closest] + node.data
			cluster_sizes[closest] += 1
			labels.append(centroids[closest])
		
		# print labels

		# Assign centroids based on datapoint labels
		for i in range(k):
			cluster_sums[i]
			cluster_sizes[i]
			new_centroids[i] = cluster_sums[i] / cluster_sizes[i]
			# new_centroids[i] = np.round(new_centroids[i])

		centroids = new_centroids

		# Debug Information
		if debug:
			print "Iteration: " + str(iterations)


			
	# We can get the labels too by calling getLabels(dataSet, centroids)
	return centroids, labels

# return k random centroids
def getRandomCentroids(nodes, numFeatures, k):
	vector_size = 784
	l = np.zeros((k, vector_size))
	i = 0
	while(i < k):
		num = randint(1, numFeatures)
		if(num not in l):
			l[i] = np.array(nodes[num].data)
			i += 1
	return l

# Function: Should Stop
# -------------
# Returns True or False if k-means is done. K-means terminates either
# because it has run a maximum number of iterations OR the centroids
# stop changing.
def shouldStop(oldCentroids, centroids, iterations):
	# if iterations > MAX_ITERATIONS: return True

	# for centroid in centroids:
	# 	print centroid
	distance = dist(oldCentroids, centroids) 

	print "Centroid change: {0}".format(distance)

	if(distance == 0):
		return True
	else:
		return False

def dist(x,y):
	return np.sqrt(np.sum((x-y)**2))

def printStats(dataset, centroids, labels, k):
	for i, centroid in enumerate(centroids):
		cluster_elems = []
		print "centroid {0} --------".format(i)
		for j, label in enumerate(labels):
			if(dist(labels[j],centroids[i]) == 0):
				cluster_elems.append(dataset.nodes[j].orig_label)
				print dataset.nodes[j].orig_label,
		most_common = Counter(cluster_elems).most_common(1)
		print "\nmost common={0}".format(most_common)
		print "# incorrectly classified: {0}".format(len(cluster_elems) - most_common[0][1])



def main():
	k = 10
	dataset = DataSet('mnist_data2.txt','mnist_labels2.txt')
	centroids, labels = kmeans(dataset, k, True)


	printStats(dataset, centroids, labels, k)

main()
