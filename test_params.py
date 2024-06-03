import alghoritm
import dataCollector
import matplotlib.pyplot as plt

data = dataCollector.DataCollection()

cross_over_rate = 0.7
mutation_rate = 0.1
size_of_pop = 10

sizes = [10, 20, 50, 100, 200, 500, 1000]
epochs = [100, 200, 500, 1000, 2000, 5000, 10000]
data.epochs = epochs
data.sizes = sizes


for size in sizes:
    alg = alghoritm.Alghoritm(mutation_rate, cross_over_rate, size)
    profit = alg.Run()
    data.alg_profits.append(profit)
    
x1 = data.sizes
y1 = data.alg_profits
plt.figure(figsize=(10, 6))
plt.plot(x1, y1)
plt.title('Impact of population size')
plt.xlabel('Size of a population')
plt.ylabel('Found solution')


size_of_pop = 10
data.alg_profits.clear()
    
x = 0.1
while x < 1:
    cross_over_rate = x
    alg = alghoritm.Alghoritm(mutation_rate, cross_over_rate, size_of_pop)
    profit = alg.Run()
    data.alg_profits.append(profit)
    data.cross_over_rates.append(cross_over_rate)
    x = x + 0.1

x1 = data.cross_over_rates
y1 = data.alg_profits
plt.figure(figsize=(10, 6))
plt.plot(x1, y1)
plt.title('Impact of cross over rate')
plt.xlabel('Cross over rates')
plt.ylabel('Found solution')

data.alg_profits.clear()
cross_over_rate = 0.7

x = 0
while x < 1:
    mutation_rate = x
    alg = alghoritm.Alghoritm(mutation_rate, cross_over_rate, size_of_pop)
    profit = alg.Run()
    data.alg_profits.append(profit)
    data.mutation_rates.append(mutation_rate)
    x = x + 0.1
    
    
print("Profits: ")
print(data.alg_profits)
print("Mutation rates: ")
print(data.mutation_rates)

x1 = data.mutation_rates
y1 = data.alg_profits
plt.figure(figsize=(10, 6))
plt.plot(x1, y1)
plt.title('Impact of mutation rate')
plt.xlabel('Mutation rates')
plt.ylabel('Found solution')
plt.show()

mutation_rate = 0.1
data.alg_profits.clear()
for epoch in epochs:
    alg = alghoritm.Alghoritm(mutation_rate, cross_over_rate, size_of_pop, epoch)
    profit = alg.Run()
    data.alg_profits.append(profit)
    data.mutation_rates.append(mutation_rate)
    
    
print("Profits: ")
print(data.alg_profits)
print("Mutation rates: ")
print(data.mutation_rates)

x1 = data.epochs
y1 = data.alg_profits
plt.figure(figsize=(10, 6))
plt.plot(x1, y1)
plt.title('Impact of the numer of epochs')
plt.xlabel('Numer of epochs')
plt.ylabel('Found solution')
plt.show()