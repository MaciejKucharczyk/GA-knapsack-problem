class Chromosome:
    """ content - zawartosc dla plecaka 
        fitness - poziom dopasowania """
    def __init__(self, content):
            self.content = content # example: [1, 0, 1, 1, 0, 0]
            self.fitness = 0
            self.profit = 0
            self.weight = 0
            self.able_to_cross = True
            
    def calculate_fitness(self, base):
        weight = 0
        profit = 0
        
        for i in range(len(self.content)):
            if self.content[i] == 1:
                weight += base.weights[i]
                profit += base.profits[i]

        self.profit = profit
        self.weight = weight
        
        self.fitness = profit
        
        if weight > base.size:
            self.fitness = round(base.size / weight, 2)