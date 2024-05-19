import random
import sys
import copy
from chromosome import Chromosome

""" Nazwy plikow z danymi """

weights = "weights.txt"
profits = "profits.txt"
size = "size.txt"
dir = "w15c1458"

class Base:
    """ Przechowywanie danych plecaka """
    def __init__(self):
        self.weights = []
        self.profits = []
        self.size = sys.maxsize

class Alghoritm:
    
    def __init__(self):
        self.mutation_rate = 0.01
        self.cross_over_rate = 0.7
        self.population = [] 
        self.selection_min = 10
        self.size_of_pop = 10
        self.base = Base()
        self.content_len = 0
    
    """ Tworzenie zawartosci dla chromosomu """
    
    def Create_chromosome(self):
        content = [1] * len(self.base.weights)
        self.content_len = len(self.base.weights)
        indexes_to_change = random.sample(range(len(content)), random.randint(0, len(content)))
        for index in indexes_to_change:
            content[index] = 0
        return content
    
    """ Tworzenie populacji - dodanie utworzonych losowo chromosomow """
    def Create_population(self):
        for i in range(self.size_of_pop):
            content = self.Create_chromosome()
            self.population.append(Chromosome(content))
            
    """ Odczyt danych z trzech plikow tekstowych """
    def Read_population(self, filename1, filename2, filename3, dir):
        weights_file = open(f"./data/{dir}/{filename1}", "r")
        for line in weights_file:
            self.base.weights.append(int(line))
        
        weights_file.close()
        
        try:
            profits_file = open(f"./data/{dir}/{filename2}", "r")
            for line in profits_file:
                self.base.profits.append(int(line))
                
            profits_file.close()
        except FileNotFoundError:
            print("File with Profits not found...")
            
        
        try:
            size_file = open(f"./data/{dir}/{filename3}", "r")
            self.base.size = int(size_file.readline())
            size_file.close()
        except FileNotFoundError:
            print("File with Size not found...")
    
    def CrossOver(self, parents):
        # Losowanie indeksu cut_point
        if self.cross_over_rate > random.random():
            # Tworzenie kopi rodziców
            parent1_copy = copy.deepcopy(parents[0])
            parent2_copy = copy.deepcopy(parents[1])
            
            cut_point = random.randint(1, len(parent1_copy.content) - 2)
            parent1_copy.content[:cut_point], parent2_copy.content[:cut_point] = parent2_copy.content[:cut_point], parent1_copy.content[:cut_point]
            
            """ Mutacja """
            self.Mutation(parent1_copy)
            self.Mutation(parent2_copy)
            
            parent1_copy.calculate_fitness(self.base)
            parent2_copy.calculate_fitness(self.base)
            
            parent1_copy.able_to_cross = False
            parent2_copy.able_to_cross = False
            
            return [parent1_copy, parent2_copy]
        
        return parents
    
    def Mutation(self, chromosome):
        if self.mutation_rate > random.random():
            print("Mutation is going on...")
            index1 = random.randint(0, self.content_len-1)
            index2 = random.randint(0, self.content_len-1)
            while index2 == index1:  # Zapewnienie, że index2 jest różny od index1
                index2 = random.randint(0, self.content_len-1)
            chromosome.content[index1], chromosome.content[index2] = chromosome.content[index2], chromosome.content[index1]
        
    def Selection(self):
        self.population = sorted(self.population, key=lambda chromosome: chromosome.fitness, reverse=True)
    
    def print_population(self, pop):
        print("Current population: ")
        for chromosome in pop:
            print("Items: ", chromosome.content, " fitness: ", chromosome.fitness, " weight: ", chromosome.weight, " profit: ", chromosome.profit)
    
    def Run_before(self): 
        self.Read_population(weights, profits, size, dir)
        self.Create_population()
        print("Initial population: ")
        for chromosome in self.population:
            chromosome.calculate_fitness(self.base)
            print("Items: ", chromosome.content, " fitness: ", chromosome.fitness)
        
        best_copy = max(self.population, key=lambda chromosome: chromosome.fitness)
        best = Chromosome(best_copy.content)
        best.calculate_fitness(self.base)
        """ MAIN LOOP """
        for _ in range(100):
            # Aktualizacja fitness i zdolnosci to reprodukcji
            for chromosome in self.population:
                chromosome.calculate_fitness(self.base)
                chromosome.able_to_cross = True
            """ SELEKCJA - sortowanie populacji ze wzgledu na fitness"""
            self.population = sorted(self.population, key=lambda chromosome: chromosome.fitness, reverse=True)           
            # print("Before: ")
            # self.print_population(self.population)
            # print("best: ", best.content, " fitness: ", best.fitness)
            """
            # Wybor rodzicow do reprodukcji:
            # Rodzic 1 jest brany z poczatku posortowanej listy z populacja
            # Rodzic 2 jest losowany
            # Kazdy chromosom moze wziac udzial w reprodukcji (w danej iteracji) tylko raz (pole able_to_cross)
            # Dzieci z danej iteracji nie sa zdolne do reprodukcji
            """
            for chromosome in self.population:
                if chromosome.able_to_cross:
                    chromosome.able_to_cross = False
                    parent = chromosome
                    while parent == chromosome and parent.able_to_cross == False:
                        parent = random.choice(self.population)
                    parent.able_to_cross = False
                    """ CROSS OVER i MUTACJA - zmiany w genach """
                    offspring = self.CrossOver([chromosome, parent])
                    self.population[self.population.index(chromosome)] = offspring[0]
                    self.population[self.population.index(parent)] = offspring[1]

                    best_chromosome = max(self.population, key=lambda chromosome: chromosome.fitness)
                    if best_chromosome.fitness > best.fitness:
                        best.content = best_chromosome.content
                        best.calculate_fitness(self.base)

                    print("Content: ",  best.content, " fitness: ", best.fitness)
                        
            # print("After: ")
            # self.Selection()
            # self.print_population(self.population)        
        
        self.population = sorted(self.population, key=lambda chromosome: chromosome.fitness, reverse=True)
        print("Final population: ")
        self.print_population(self.population)
        if self.population != []:
            print("Best : ")
            print("Items: ", best.content, " fitness: ", best.fitness, " weight: ", best.weight, " profit: ", best.profit)
        else:
            print("No solution found, check input files")
            
    def Selection_roulette_wheel(self):
        total_fitness = sum(chromosome.fitness for chromosome in self.population)
        pick = random.uniform(0, total_fitness)
        current = 0
        for chromosome in self.population:
            current += chromosome.fitness
            if current > pick:
                return chromosome
        
    def Run(self): 
        self.Read_population(weights, profits, size, dir)
        self.Create_population()
        
        print("Initial population: ")
        for chromosome in self.population:
            chromosome.calculate_fitness(self.base)
            print("Items: ", chromosome.content, " fitness: ", chromosome.fitness)
        
        best_copy = max(self.population, key=lambda chromosome: chromosome.fitness)
        best = Chromosome(best_copy.content)
        best.calculate_fitness(self.base)
        """ MAIN LOOP """
        for _ in range(1000):
            new_population = []
            # Aktualizacja fitness i zdolnosci to reprodukcji
            for chromosome in self.population:
                chromosome.calculate_fitness(self.base)
                chromosome.able_to_cross = True
            """ SELEKCJA - ruletka
            === Wybor rodzicow do reprodukcji:
            - rodzice sa wybierani za pomoca kola ruletki
            - w danej iteracji MAIN LOOP tworzona jest nowa populacja
            - nowa populacja jest tworzona z dzieci poprzedniej populacji
            - nowa populacja zastepuje poprzednia populacje, kiedy beda miec takie same rozmiary
            """
            
            while len(new_population) < len(self.population):
                parent1 = self.Selection_roulette_wheel()
                parent2 = self.Selection_roulette_wheel()
                """ CROSS OVER i MUTACJA - zmiany w genach """
                offspring = self.CrossOver([parent1, parent2])
                new_population.append(offspring[0])
                if len(new_population) < len(self.population):
                    new_population.append(offspring[1])

            self.population = copy.deepcopy(new_population)
            
            print("New population: ")
            for chromosome in self.population:
                chromosome.calculate_fitness(self.base)
                print("Items: ", chromosome.content, " fitness: ", chromosome.fitness)
            
            best_chromosome = max(self.population, key=lambda chromosome: chromosome.fitness)
            if best_chromosome.fitness > best.fitness:
                best.content = best_chromosome.content
                best.calculate_fitness(self.base)

            print("Best solution: ")
            print("Content: ",  best.content, " fitness: ", best.fitness)
                        
            # print("After: ")
            # self.Selection()
            # self.print_population(self.population)        
        
        self.population = sorted(self.population, key=lambda chromosome: chromosome.fitness, reverse=True)
        print("Final population: ")
        self.print_population(self.population)
        if self.population != []:
            print("Best : ")
            print("Items: ", best.content, " fitness: ", best.fitness, " weight: ", best.weight, " profit: ", best.profit)
        else:
            print("No solution found, check input files")