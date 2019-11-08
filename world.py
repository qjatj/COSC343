#!/usr/bin/env python

# Import statements
from cosc343world import Creature, World
import numpy as np
import random
import matplotlib.pyplot as plt

numGenerations = 100    # Number of generations to run
numTurns = 100          # Number of turns in each generation
worldType = 1           # World type
gridSize = 48           # World size
repeatableMode = False  # Removes randomness for testing if set to true
plotlife = []           # Use for plotting average life graph
plotfitness = []        # Use for plotting average fitness graph


class MyCreature(Creature):

    # Constructor
    def __init__(self, numPercepts, numActions):
        self.chromosome = np.random.uniform(0, 1, 11)
        Creature.__init__(self)


    # This is the implementation of the agent function that is called on every turn, giving
    # creatures a chance to perform an action.  AgentFunction takes its parameters
    # from the chromosome and it produces a set of actions from provided percepts
    #
    # Input: percepts - a list of percepts
    #        numAction - the size of the actions list that needs to be returned
    def AgentFunction(self, percepts, numActions):
        actions = [0] * (numActions)    # Initialise actions list and set values as 0

        # If on red strawberry, increase probability of eating by 85%
        if percepts[4] == 2:
            actions[9] += 0.85
        # If on green strawberry, increase probability of eating by 25%
        elif percepts[4] == 1:
            actions[9] += 0.25
        # Otherwise remove eating action from action list
        else:
            actions[9] -= self.chromosome[9]

        for i in range(len(percepts)):
            # If food in neighbouring square, increase probability of moving to it by 50%
            if percepts[i] == 3:
                actions[i] += 0.5
            # If other creature nearby, don't move to that square
            elif percepts[i] == 2:
                actions[i] -= self.chromosome[i]
            # If monster nearby, don't move to that square
            elif percepts[i] == 1:
                actions[i] -= self.chromosome[i]
            # Otherwise, pick random probability of moving to square between 0% and 30%
            #else:
                #actions[i] += np.random.uniform(0, 0.3, 1)


        for x in range(len(self.chromosome)):
            actions[x] += self.chromosome[x]

        return actions

# Selection method to pick fittest parent out of 5 for new population
def Select(old_population):
    # Pick fittest parent as a random parent from old population
    fittest = random.choice(old_population)
    # For 4 new parents, if new parent has a larger fitness score, replace as fittest parent
    for i in range(4):
        creature = random.choice(old_population)
        if creature.score > fittest.score:
            fittest = creature
    # Return fittest parent out of 5 parents
    return fittest

# Crossover method that mixes the chromosome of 2 fit parents to create child creature
def CrossOver(successors):
    child = []


    cutpoint = random.randint(1, len(successors[0].chromosome) - 1)  # Pick random cutpoint
    left = random.randint(0, 1)     # 0 if first successor DNA is on left, else 1

    if left == 0:
        child.extend(successors[0].chromosome[:cutpoint])   # Use first successor DNA up to cutpoint
        child.extend(successors[1].chromosome[cutpoint:])   # Use second successor DNA up to cutpoint
    else:
        child.extend(successors[1].chromosome[:cutpoint])   # Use second successor DNA up to cutpoint
        child.extend(successors[0].chromosome[cutpoint:])   # Use second successor DNA up to cutpoint

    return child

# Mutation method that mutates child chromosomes at random chance for randomness
def Mutation(child):
    # For all values of chromosome, pick random value between 0% - 100%.
    # If value is less than 6%, mutate that DNA with random value
    for i in range(8):
        if random.randint(0, 100) < 6:
            mutatedDNA = np.random.uniform(0, 1)
            child.chromosome[i] = mutatedDNA


# newPopulation method that creates new population from old population,
# graphing the old population at every generation
def newPopulation(old_population):
    global numTurns

    nSurvivors = 0      # Number of survivors at generation
    avgLifeTime = 0     # Average life time at generation
    fitnessScore = 0    # Total fitness score at generation


    for individual in old_population:

        energy = individual.getEnergy()     # 0 if creature is dead
        dead = individual.isDead()          # true if individual is dead
        survivalPoints = 0                  # Survival points for individual
        endEnergy = 0                       # Ending energy for individual

        # If individual has died
        if dead:
            timeOfDeath = individual.timeOfDeath()      # Store time of death
            avgLifeTime += timeOfDeath                  # Add to total life time
            survivalPoints += timeOfDeath               # Add death time to survival points
        # If individual hasn't died
        else:
            nSurvivors += 1                             # Add to survivors
            avgLifeTime += numTurns                     # Add numTurns to total life time
            survivalPoints = numTurns * 1.4             # Add numTurns plus bonus to survival points
            endEnergy = energy * 2                      # Add energy plus bonus points to end energy

        individual.score = survivalPoints + endEnergy
        fitnessScore += individual.score

    # Statistics for graphing
    avgLifeTime = float(avgLifeTime)/float(len(population))
    avgfitnessScore = fitnessScore/float(len(population))
    plotlife.append(avgLifeTime)
    plotfitness.append(avgfitnessScore)


    print("Simulation stats:")
    print("  Survivors    : %d out of %d" % (nSurvivors, len(population)))
    print("  Avg life time: %.1f turns" % avgLifeTime)


    new_population = []

    # While new population is not equal to old population
    while len(new_population) < len(population):
        successors = []
        # While there isn't 2 successors
        while len(successors) < 2:
            successors.append(Select(old_population))                   # Add new successor using selection method

        child = MyCreature(numCreaturePercepts, numCreatureActions)     # Create child object
        child.chromosome = CrossOver(successors)                        # Perform crossover using successors
        Mutation(child)                                                 # Mutate child at random

        new_population.append(child)                                    # Append child to new population

    return new_population


plt.close('all')
fh=plt.figure()

# Create the world.  Representaiton type choses the type of percept representation (there are three types to chose from);
# gridSize specifies the size of the world, repeatable parameter allows you to run the simulation in exactly same way.
w = World(worldType=worldType, gridSize=gridSize, repeatable=repeatableMode)

#Get the number of creatures in the world
numCreatures = w.maxNumCreatures()

#Get the number of creature percepts
numCreaturePercepts = w.numCreaturePercepts()

#Get the number of creature actions
numCreatureActions = w.numCreatureActions()

# Create a list of initial creatures - instantiations of the MyCreature class that you implemented
population = list()
for i in range(numCreatures):
   c = MyCreature(numCreaturePercepts, numCreatureActions)
   population.append(c)

# Pass the first population to the world simulator
w.setNextGeneration(population)

# Runs the simulation to evalute the first population
w.evaluate(numTurns)

# Show visualisation of initial creature behaviour
w.show_simulation(titleStr='Initial population', speed='normal')

for i in range(numGenerations):
    print("\nGeneration %d:" % (i+1))

    # Create a new population from the old one
    population = newPopulation(population)

    # Pass the new population to the world simulator
    w.setNextGeneration(population)

    # Run the simulation again to evalute the next population
    w.evaluate(numTurns)

    # Show visualisation of final generation
    if i==numGenerations-1:
        w.show_simulation(titleStr='Final population', speed='normal')


# Use for plotting average life
#plt.plot(plotlife)
#plt.ylabel('Avg life for each evolution')
#plt.xlabel('Amount of evolutions')
#plt.show()

# Use for plotting average fitness
plt.plot(plotfitness)
plt.ylabel('Avg Fitness for each evolution')
plt.xlabel('Amount of evolutions')
plt.show()
