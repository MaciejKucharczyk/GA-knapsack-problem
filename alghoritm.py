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
            cut_point = random.randint(1, len(parents[0].content) - 2)
            parents[0].content[:cut_point], parents[1].content[:cut_point] = parents[1].content[:cut_point], parents[0].content[:cut_point]
            
            """ Mutacja """
            self.Mutation(parents[0])
            self.Mutation(parents[1])
            
            parents[0].calculate_fitness(self.base)
            parents[1].calculate_fitness(self.base)
            
            parents[0].able_to_cross = False
            parents[1].able_to_cross = False
        
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
        for _ in range(100):
            # Aktualizacaja fitness i zdolnosci to reprodukcji
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
                    self.CrossOver([chromosome, parent])

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
            