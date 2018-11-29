from random import *
import numpy as np

populationNumber = int(input("Enter Population Number: "))
mutation = float(input("Enter Mutation Percentage: "))

sumUpTO = int(input("Enter Sum Up To: "))
multiplyUpTo = int(input("Enter Multiply Up To: "))

numberOfCards = 10


def generateDNA():
    p_dna = []
    for x in range(numberOfCards):
        p_dna.append(getRandomNumber(1,13))
    p_dna.append(getRandomNumber(0,numberOfCards))
    return p_dna


def getRandomNumber(p_lowerBound, p_upperBound):
    return randint(p_lowerBound, p_upperBound)


def initPopulation():
    p_pop = []
    for x in range(populationNumber):
        p_pop.append([generateDNA(), 0])
    return p_pop


def calculateFitness(p_pop):
    for i in range(populationNumber):
        p_pop[i][1] = fitness(p_pop[i][0])
    return p_pop


def fitness(p_dna):
    return (sumFitness(p_dna) + multFitness(p_dna)) / 2


def sumFitness(p_dna):
    return 1 - abs(36 - sumFirst(p_dna)) / 86


def sumFirst(p_dna):
    temp_sum = 0
    for x in range(p_dna[numberOfCards]):
        temp_sum = temp_sum + p_dna[x]
    return temp_sum


def multFitness(p_dna):
    mult = multiplySecond(p_dna)
    if mult == 0:
        return 0
    score = 1 - abs(360 - mult) / (13 * 13 * 13 * 13 * 12 * 12 * 12 * 12 * 11 * 11)
    if score == 1:
        return score
    #while score > 0.9:
     #   score -= 0.9
      #  score *= 10
    return score


def multiplySecond(p_dna):
    temps = 1
    for x in range(p_dna[numberOfCards], numberOfCards):
        temps *= p_dna[x]
    return temps


def checkPopulation(p_pop):
    for i in range(populationNumber):
        if p_pop[i][1] == 1:
            return i
    return -1


def selectParents(p_pop):
    parents = list(range(populationNumber))
    weights = [i[1] for i in calculateProbabilities(p_pop)]
    parents = np.random.choice(parents, 2, False, weights)
    parents = [p_pop[parents[0]][0], p_pop[parents[1]][0]]
    return parents


def calculateProbabilities(p_pop):
    mySum = 0
    for x in range(populationNumber):
        mySum += p_pop[x][1]
    for x in range(populationNumber):
        p_pop[x][1] = p_pop[x][1] / mySum
    return p_pop


def crossover(p_parents):
    p1 = p_parents[0]
    p2 = p_parents[1]
    child = list()
    for i in range(numberOfCards + 1):
        p = getRandomNumber(0,1)
        if p == 1:
            child.append(p1[i])
        else:
            child.append(p2[i])
    return child


def mutate(p_dna):
    for x in range(numberOfCards + 1):
        if random() < mutation:
            if x == numberOfCards:
                p_dna.pop()
                p_dna.append(getRandomNumber(0,numberOfCards))
            else:
                p_dna.pop(x)
                p_dna.insert(x, getRandomNumber(1,13))
    return p_dna


def generateNewPopulation(p_pop):
    newPop = list()
    for x in range(populationNumber):
        parents = selectParents(p_pop)
        child = crossover(parents)
        child = mutate(child)
        newPop.append([child, 0])
    newPop = checkPopulationConsistency(newPop)
    return newPop


def checkPopulationConsistency(p_pop):
    for i in range(populationNumber):
        p = p_pop[i][0]
        for j in range(numberOfCards):
            count = 1
            for k in range(j + 1, numberOfCards):
                if p[j] == p_pop[i][0][k]:
                    count += 1
                    if count > 4:
                        n = getRandomNumber(1,13)
                        while n == p[j]:
                            n = getRandomNumber(1,13)
                        p_pop[i][0][k] = n
                        checkPopulation(p_pop)
    return p_pop


def getMaxFitness(p_pop):
    return max([i[1] for i in p_pop])


def getBestSoFar(p_pop):
    maxF = getMaxFitness(p_pop)
    for i in range(populationNumber):
        if p_pop[i][1] == maxF:
            return p_pop[i][0]


def printPopulation(p_pop, counter):
    bestSoFar = getBestSoFar(p_pop)
    indexOfBestSoFar = bestSoFar[numberOfCards]
    print("EPOCH: " + str(counter) + "\n")
    print("MAX FITNESS: " + str(getMaxFitness(p_pop)) + "\n")
    print("BEST SO FAR: " + str(bestSoFar) + "\n")
    print("SUM: " + str(sum(bestSoFar[:indexOfBestSoFar])))
    print("MULTIPLICATION: " + str(mult(bestSoFar[indexOfBestSoFar:numberOfCards])))
    print("POPULATION:" + "\n")
    for i in range(populationNumber):
        print(str(Population[i][0]) + " Fitness: " + str(Population[i][1]))
    return


def mult(p_list):
    result = 1
    for i in p_list:
        result *= i
    return result


counter = 0
Population = initPopulation()
Population = calculateFitness(Population)

pos = -1

while pos == -1:
    counter += 1
    printPopulation(Population, counter)
    Population = generateNewPopulation(Population)
    Population = calculateFitness(Population)
    print(Population)
    pos = checkPopulation(Population)

print("\n\n\nHURRAY!!!\n\n")
print("ITERATIONS: " + str(counter) + "\n\n")
result = Population[pos]
indexOfResult = result[0][numberOfCards]
print("RESULT: " + str(result[0]))
print("FIRST GROUP: " + str(result[0][:indexOfResult]))
print("SUM: " + str(sum(result[0][:indexOfResult])))
print("SECOND GROUP: " + str(result[0][indexOfResult:numberOfCards]))
print("MULTIPLICATION: " + str(mult(result[0][indexOfResult:numberOfCards])))
