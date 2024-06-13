from utilities import *
from fitness_utilities import *
import random

population_size = 100  # Size of the population
generations = 500  # Number of generations
mut_rate = 0.075  # Mutation rate


def generate_initial_population():
    # Generate the initial population of schedules.
    pop = []
    for individual in range(population_size):
        s = generate_schedule()
        if s != -1:
            pop.append(s)
    return pop


def calculate_fitness(schedule):
    # Calculate the fitness of a schedule.
    conflicts = 0
    conflicts += count_prof_room_conflicts(schedule)

    # Calculate conflicts due to duplicate courses, oversized lectures, and adjacent day courses
    conflicts += count_duplicate_courses_in_schedule(schedule)
    conflicts += count_oversized_lectures(schedule)
    conflicts += count_adjacent_day_courses(schedule)

    return 1 / (1 + conflicts)  # Inverse of conflicts, higher fitness for fewer conflicts


def crossover(parent1, parent2):
    # Perform crossover operation between two parent schedules.
    crossover_point = random.randint(1, min(len(parent1), len(parent2)) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


def calculate_population_fitness(pop):
    # Calculate the fitness of each individual in the population.
    pop_fitness = []
    for schedule in pop:
        fitness = calculate_fitness(schedule)
        pop_fitness.append((schedule, fitness))
    return pop_fitness


def mutate(schedule):
    # Apply mutation operation to a schedule.
    lectures = []
    for day_schedule in schedule:
        for room_schedule in day_schedule:
            for slot in room_schedule:
                if slot is not None:
                    course, _ = slot
                    if course.course_type == "T":
                        lectures.append(slot)

    if len(lectures) < 2:
        print("Not enough lectures to perform a swap.")
        return schedule

    random.shuffle(lectures)
    lecture1, lecture2 = lectures[:2]

    for day_schedule in schedule:
        for room_schedule in day_schedule:
            for i, slot in enumerate(room_schedule):
                if slot == lecture1:
                    room_schedule[i] = lecture2
                elif slot == lecture2:
                    room_schedule[i] = lecture1

    return schedule


def genetic_algorithm():
    # Perform the genetic algorithm for scheduling.

    # Generate the initial population
    population = generate_initial_population()

    # Iterate through generations
    for generation in range(generations):
        # Calculate fitness for each individual in the population
        population_fitness = calculate_population_fitness(population)
        population_fitness.sort(key=lambda x: x[1], reverse=True)  # Sort by fitness, highest first

        # Print generation information
        print("\nGeneration:", generation)
        print("fittest: " + str(population_fitness[0][1]))

        # Select parents for crossover
        parent1, _ = population_fitness[0]
        parent2, _ = population_fitness[1]
        child1, child2 = crossover(parent1, parent2)

        # Print fitness of children
        # print("Child 1 fitness: " + str(calculate_fitness(child1)))
        # print("Child 2 fitness: " + str(calculate_fitness(child2)))

        # Replace worst individual(s) with children if they have higher fitness
        index_of_worst = population.index(population_fitness[-1][0])
        if calculate_fitness(child1) > calculate_fitness(population[index_of_worst]):
            population[index_of_worst] = child1
        if calculate_fitness(child2) > calculate_fitness(population[index_of_worst]):
            population[index_of_worst] = child2

        # Re-calculate population fitness after crossover
        population_fitness = calculate_population_fitness(population)
        population_fitness.sort(key=lambda x: x[1], reverse=True)  # Sort by fitness

        # Print worst fitness and fittest after crossover
        # print("WORST fitness: " + str(population_fitness[-1][1]))
        # print("fittest: " + str(population_fitness[0][1]))

        # Perform mutation
        if random.random() < mut_rate:
            index_of_worst = population.index(population_fitness[-1][0])
            if index_of_worst != population.index(population_fitness[0][0]):
                mutated_individual = mutate(population_fitness[-1][0])
                if calculate_fitness(mutated_individual) > calculate_fitness(population[index_of_worst]):
                    population[index_of_worst] = mutated_individual

    # Get the best schedule and its fitness
    best_schedule, best_fitness = population_fitness[0]
    print("Best Schedule for current number of generations:")
    # Print the best schedule for each day
    for each_day_schedule, day_name in zip(best_schedule, week):
        print_day(each_day_schedule, [room.room_id for room in sample_rooms], slots, day_name)


if __name__ == "__main__":
    genetic_algorithm()
