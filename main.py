import random


# Initialization of the oldest individuals
class Individual:
    def __init__(self, k, C, A, g_min, g_max, r_min):
        self.k = k
        self.C = C
        self.A = A
        self.g_min = g_min
        self.g_max = g_max
        self.r_min = r_min
        self.n = len(A)
        self.code = [0 for _ in range(self.n)]
        self.g1 = random.randrange(self.g_min, self.g_max + 1)
        self.g2 = random.randrange(self.g_min, self.g_max + 1)

        self.beginningGreen1 = random.randrange(self.n - self.g1 - self.g2 - self.r_min)
        self.beginningGreen2 = random.randrange(self.beginningGreen1 + self.g1 + self.r_min, self.n - self.g2)

        for i in range(self.g1):
            self.code[self.beginningGreen1 + i] = 1
        for i in range(self.g2):
            self.code[self.beginningGreen2 + i] = 1
        self.r1 = -1
        self.r2 = -1
        self.beginningRed1 = -1
        self.beginningRed2 = -1
        if self.code[0] == 0:
            self.beginingRed1 = 0
            self.r1 = self.beginningGreen1
            self.beginningRed2 = self.beginningGreen1 + self.g1
            self.r2 = self.beginningGreen2 - self.beginningRed1
        else:
            self.beginningRed1 = self.beginningGreen1 + self.g1
            self.r1 = self.beginningGreen2 - self.beginningRed1
            self.beginningRed2 = self.beginningGreen2 + self.g2
            self.r2 = self.n - self.beginningRed2

        self.fitness = self.fitnessFunction()

    # Determines how good an individual is
    # According to the formula, the one with the best result is calculated, she is the best individual
    def fitnessFunction(self):
        val = 0
        for i in range(self.n):
            val += self.A[i] * self.code[i]
        return val

    def __lt__(self, other):
        return self.fitness >= other.fitness

# Checks that the restrictions have been met, to check that the individual is good
def isFeasible(individual):
    if individual.g1 < individual.g_min or individual.g1 > individual.g_max:
        return False
    if individual.g2 < individual.g_min or individual.g2 > individual.g_max:
        return False
    if individual.r1 < individual.r_min:
        return False
    if individual.r2 < individual.r_min:
        return False

    number_of_green_light_cycles = 0
    number_of_red_light_cycles = 0

    for i in range(individual.n - 1):
        if individual.code[i] == 0 and individual.code[i + 1] == 1:
            number_of_green_light_cycles += 1
        if individual.code[i] == 1 and individual.code[i + 1] == 0:
            number_of_red_light_cycles += 1
    if number_of_green_light_cycles == individual.k or number_of_red_light_cycles == individual.k:
        return True
    else:
        return False

    return True

# Update values after each individual determination round
def updateValues(individual):
    r1 = -1
    g1 = -1
    r2 = -1
    g2 = -1
    if individual.code[0] == 0:
        r1 = 0
        for i in range(individual.n - 1):
            if individual.code[i] == 0 and individual.code[i + 1] == 1:
                if g1 == -1:
                    g1 = i + 1
                elif g2 == -1:
                    g2 = i + 1
            if individual.code[i] == 1 and individual.code[i + 1] == 0:
                if r2 == -1:
                    r2 = i + 1
        beginningGreen1 = r1
        beginningGreen2 = g1 + r1 + r2
        beginningRed1 = 0
        beginningRed2 = g1 + r1

    else:
        g1 = 0
        for i in range(individual.n - 1):
            if individual.code[i] == 0 and individual.code[i + 1] == 1:
                if g2 == -1:
                    g2 = i + 1

            if individual.code[i] == 1 and individual.code[i + 1] == 0:
                if r1 == -1:
                    r1 = i + 1
                elif r2 == -1:
                    r2 = i + 1
        beginningGreen1 = 0
        beginningGreen2 = g1 + r1
        beginningRed1 = g1
        beginningRed2 = g1 + r1 + g2
    individual.g1 = g1
    individual.g2 = g2
    individual.r1 = r1
    individual.r2 = r2
    individual.beginningGreen1 = beginningGreen1
    individual.beginningGreen2 = beginningGreen2
    individual.beginningRed1 = beginningRed1
    individual.beginningRed2 = beginningRed2

# Execution of mutations, if any
def mutation(individual, mutationRate):
    if random.uniform(0, 1) <= mutationRate:
        i = random.randrange(individual.n)
        individual.code[i] = abs(individual.code[i] - 1)

        updateValues(individual)

        if not isFeasible(individual):
            individual.code[i] = abs(individual.code[i] - 1)
            updateValues(individual)

# Breeding selection of two individuals
# Tournament selection - a parameter of the length of the tournament where each time the
# only one is taken and the fitness of one individual is compared with other individuals
# The one that is best suited, she will be chosen
def selection(population, population_size, tournament_size):
    bestI = -1
    bestVal = 0
    for _ in range(tournament_size):
        i = random.randrange(population_size)
        if population[i].fitness < bestVal:
            bestVal = population[i].fitness
            bestI = i
    return bestI

# Crossing of individuals
def crossover(parent1, parent2, child1, child2):
    n = parent1.n
    for i in range(n):
        child1.code[i] = 0
        child2.code[i] = 0
    for i in range(0, parent1.g1):
        child1.code[parent2.beginningGreen1 + i] = 1
    for i in range(0, parent1.g2):
        if parent2.beginningGreen2 + i >= n:
            break
        child1.code[parent2.beginningGreen2 + i] = 1
    for i in range(0, parent2.g1):
        child2.code[parent1.beginningGreen1 + i] = 1
    for i in range(0, parent2.g2):
        if parent1.beginningGreen2 + i >= n:
            break
        child2.code[parent1.beginningGreen2 + i] = 1

# Initialization and work with tournament selection
def GA(k, C, A, g_min, g_max, r_min):
    POPULATION_SIZE = 300
    ELITISM_SIZE = 100
    MUTATION_RATE = 0.1
    TOURNAMENT_SIZE = 20
    MAX_ITER = 1500
    population = [Individual(k, C, A, g_min, g_max, r_min) for _ in range(POPULATION_SIZE)]
    new_population = [Individual(k, C, A, g_min, g_max, r_min) for _ in range(POPULATION_SIZE)]

    best_individual = population[0]
    iter_updated = 0
    for iteration in range(MAX_ITER):
        population.sort()
        if best_individual.fitness < population[0].fitness:
            best_individual = population[0]
            iter_updated = iteration
        if iteration % 10 == 0:
            print(best_individual.code)
            print(best_individual.fitness)
            print('-------------------------')
        if iteration - iter_updated > 100:
            return best_individual
        for i in range(ELITISM_SIZE):
            new_population[i] = population[i]
        for i in range(ELITISM_SIZE, POPULATION_SIZE, 2):
            i1 = selection(population, POPULATION_SIZE, TOURNAMENT_SIZE)
            i2 = selection(population, POPULATION_SIZE, TOURNAMENT_SIZE)
            crossover(population[i1], population[i2], new_population[i], new_population[i + 1])
            mutation(new_population[i], MUTATION_RATE)
            mutation(new_population[i + 1], MUTATION_RATE)
            new_population[i].fitness = new_population[i].fitnessFunction()
            new_population[i + 1].fitness = new_population[i + 1].fitnessFunction()

        new_population[:] = population[:]
    population.sort()
    if best_individual.fitness < population[0].fitness:
        best_individual = population[0]
    return best_individual

# The main program that sorts the string in ascending order
if __name__ == '__main__':
    k = 2
    C = 10
    A = [0, 0, 3, 4, 3, 3, 3, 0, 2, 1, 0, 0, 0, 0, 0, 3, 4, 3, 0, 0]
    g_min = 3
    g_max = 7
    r_min = 2

    P = GA(k, C, A, g_min, g_max, r_min)

    print(P.code)
    print(P.fitness)