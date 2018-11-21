from random import *
import numpy as np

Target = input("Enter Target Phrase: ")
populationNumber = int(input("Enter Population Number: "))
mutation = float(input("Enter Mutation Percentage: "))

stringLength = len(Target)
offspring = int(stringLength / 2)
# offspring = int(randint(0, stringLength-1))
Population = []


def generateDNA():
    p_dna = ''
    for x in range(stringLength):
        p_dna = p_dna + getRandomChar()
    return p_dna


def getRandomChar():
    randomChar = randint(97, 123)
    if randomChar == 123:
        randomChar = 32
    return chr(randomChar)


def printPopulation(p_pop, p_counter, p_target):
    print("\n\n\nTARGET: " + p_target)
    print("EPOCH: " + str(p_counter) + "\n\nPOPULATION:\n")
    for x in range(populationNumber):
        print(p_pop[x][0])


def crossover(parents):
    i = offspring
    p1 = parents[0]
    p2 = parents[1]
    child = (p1[:i] + p2[i:stringLength])
    # mutate(child)
    return child


def mutate(p_dna, p_target):
    for x in range(stringLength):
        if p_dna[x] == p_target[x]:
            pass
        elif random() < mutation:
            p_dna = p_dna[:x] + getRandomChar() + p_dna[x + 1:]
    return p_dna


def initPopulation(p_pop):
    for x in range(populationNumber):
        p_pop.append([generateDNA(), 0])
    return p_pop


def fitness(p_dna, p_target):
    value = 0
    for x in range(stringLength):
        if p_dna[x] == p_target[x]:
            value += 1
    return value


def normalizeFitness(p_pop):
    sumOfFitness = 0
    for x in range(populationNumber):
        sumOfFitness += p_pop[x][1]
    for x in range(populationNumber):
        if sumOfFitness != 0:
            p_pop[x][1] = (p_pop[x][1] / sumOfFitness)
    return p_pop


def evaluateFitness(p_pop, p_target):
    for x in range(populationNumber):
        p_pop[x][1] = fitness(p_pop[x][0], p_target)
    normalized = normalizeFitness(p_pop)
    return normalized


def checkPopulation(p_pop, p_target):
    for x in range(populationNumber):
        if p_pop[x][0] == p_target:
            return 1
    return 0


def selectParents(p_pop):
    parents = [i[0] for i in p_pop]
    weights = [i[1] for i in p_pop]
    try:
        return np.random.choice(parents, 2, False, weights)
    except:
        return [p_pop[0], p_pop[1]]


def generateNewPopulation(p_pop, p_target):
    newPop = []
    for x in range(populationNumber):
        parents = selectParents(p_pop)
        child = crossover(parents)
        child = mutate(child, p_target)
        newPop.append([child, 0])
    return newPop


def executeGeneticAlgorithm(p_pop, p_target):
    if checkPopulation(p_pop, p_target) == 1:
        return 1
    else:
        p_pop = evaluateFitness(p_pop, p_target)
        return generateNewPopulation(p_pop, p_target)


counter = 0
initPopulation(Population)
if checkPopulation(Population, Target) == 1:
    Population = 1
    printPopulation(Population, counter, Target)

while Population != 1:
    counter += 1
    printPopulation(Population, counter, Target)
    Population = executeGeneticAlgorithm(Population, Target)

print("\n\nFOUND: " + Target + "\n")
counter += 1
print("ITERATIONS: " + str(counter) + "\n")

print("NOTE: in order to find the target phrase, look for it in the last population generated.\n\n")

print("HURRAY!!!!\n\n\n")


var = input("Press any key to exit")
