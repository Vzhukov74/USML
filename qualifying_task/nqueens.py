# -*- coding: utf-8 -*-
import random
import threading
import time

#for sorting array of Chromosome objects
def byFitnessKey(chromosome):
    return chromosome.fitness

class Solver_8_queens:

    def __init__(self, pop_size=800, cross_prob=0.22, mut_prob=0.09):
        self.popSize = pop_size
        self.crossProb = cross_prob
        self.mutProb = mut_prob
        self.chromosomes = []

    def solve(self, min_fitness=0.8, max_epochs=100):
        self.chromosomes = self.createChromosomeSets(self.popSize)

        best_fit=None
        epoch_num = 0
        visualization=None

        while True:
            epoch_num += 1
            print("current epoch: " + str(epoch_num))

            self.calculateFitness()
            self.rouletteSelection()
            for chromosome in self.chromosomes:
                if chromosome.fitness == 1:
                    best_fit = chromosome.fitness
                    visualization = chromosome.createVisualization()
                    return best_fit, epoch_num, visualization
                elif min_fitness is not None:
                    if chromosome.fitness >= min_fitness:
                        best_fit = chromosome.fitness
                        visualization = chromosome.createVisualization()
                        return best_fit, epoch_num, visualization

            self.crossover()
            self.mutation()

            if epoch_num == max_epochs:
                break

        self.chromosomes.sort(key = byFitnessKey, reverse = True)
        best_fit = self.chromosomes[0].fitness
        epoch_num = max_epochs
        visualization = self.chromosomes[0].createVisualization()
        return best_fit, epoch_num, visualization

    def calculateFitness(self):
        for chromosome in self.chromosomes:
            chromosome.calculateFitness()

    def rouletteSelection(self):
        sumFitness = 0
        self.chromosomes.sort(key = byFitnessKey, reverse = True)

        for chromosome in self.chromosomes:
            sumFitness += chromosome.fitness

        threads = []
        for i in range(0, self.chromosomes.__len__()):
            thread = RouletteSelectionThread(self.chromosomes, sumFitness)
            threads.append(thread)
            thread.start()

        while threading.activeCount() > 1:
            time.sleep(1)

        selectedChromosomes = []
        for thread in threads:
            selectedChromosomes.append(thread.selectedChromosome)

        self.chromosomes = selectedChromosomes

    def crossover(self):
        for index in range(0, self.chromosomes.__len__(), 2):
            if index > self.chromosomes.__len__() - 2:
                break
            else:
                nextIndex = index + 1

                randomNumber = random.uniform(0.0, 1.0)
                if randomNumber > self.crossProb:
                    self.doCrossing(index, nextIndex)


    def doCrossing(self, index1, index2):
        firstChromosome = self.chromosomes[index1]
        secondChromosome = self.chromosomes[index2]

        randomInt = random.randint(0, 7)

        child1 = []
        child2 = []

        for i in range(0, randomInt):
            child1.append(firstChromosome.genes[i])
            child2.append(secondChromosome.genes[i])

        for i in range(randomInt, 8):
            child1.append(secondChromosome.genes[i])
            child2.append(firstChromosome.genes[i])

        self.chromosomes[index1] = Chromosome(child1)
        self.chromosomes[index2] = Chromosome(child2)

    def mutation(self):
        for index in range(self.chromosomes.__len__()):
            randomNumber = random.uniform(0.0, 1.0)
            if randomNumber > self.mutProb:
                self.doMutation(index)

    def doMutation(self, index):
        randomInt = random.randint(0, 7)
        self.chromosomes[index].genes[randomInt] = random.randint(0, 7)

    def createChromosomeSets(self, pop_size):
        chromosomeSets = []

        for _ in range(pop_size):
            chromosomeSets.append(Chromosome.createChromosome())

        return chromosomeSets

class Chromosome():
    def __init__(self, genes):
        self.genes = genes
        self.fitness = 0

    def calculateFitness(self):
        fit = 0
        for i in range(8):
            for j  in range((i + 1), 8):
                if self.genes[i] == self.genes[j]:
                    fit += 1
                elif abs(self.genes[i] - self.genes[j]) == abs(i - j):
                    fit += 1

        fit = (1 + fit) ** -1
        self.fitness = fit

    def createVisualization(self):
        visualization = ''
        chars = list()
        for r in range(8):
            for c in range(8):
                gene = self.genes[r]
                if gene == c:
                    chars.append("Q")
                else:
                    chars.append("+")
            if r != 7:
                chars.append("\n")

        return ''.join(chars)

    def createChromosome():
        genes = []
        for _ in range(8):
            randomInt = random.randint(0, 7)
            genes.append(randomInt)

        return Chromosome(genes)

class RouletteSelectionThread(threading.Thread):
    def __init__(self, chromosomes, sumFitness):
        threading.Thread.__init__(self)
        self.chromosomes = chromosomes
        self.sumFitness = sumFitness

    def run(self):
        randomNumber = random.uniform(0.0, self.sumFitness)
        partialSum = 0.0

        index = 0
        while partialSum < randomNumber:
            partialSum += self.chromosomes[index].fitness
            index += 1

        self.selectedChromosome = self.chromosomes[index - 1]
