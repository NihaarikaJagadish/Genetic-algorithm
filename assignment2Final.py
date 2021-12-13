import math
from PIL import Image, ImageDraw
import random
import math

POPULATION_SIZE = 100

#Each object of the this class represents one state in the population
class Individual(object):
    def __init__(self, chromosome):
        '''The chromosome of each state are defined by the rectangles that are generated.
        Each rectangle is then defined by x1, y1, x2, y2 and the color from (105,105,105,125)
        '''
        self.chromosome = chromosome 
        self.fitness = self.cal_fitness()
        
    @classmethod
    def mutated_genes(self): # This function is to randomly generate a rectangle
        x1 = random.randint(0, 21)
        y1 = random.randint(0, 21)
        size = random.randint(1,5)
        shape = [(x1,y1),(x1 + size,y1+ size)] 
        return shape

    @classmethod
    def create_gnome(self):#Creating rectangle for each state in a population
        return [self.mutated_genes() for _ in range(100)]


    def mate(self, par2): # Responsible for mating. Both Cross over and mutation
        child_chromosome = []
        for gp1, gp2 in zip(self.chromosome, par2.chromosome):
            prob = random.random()
            if prob < 0.45: #CrossOver
                child_chromosome.append(gp1)
            elif prob < 0.90: #CrossOver
                child_chromosome.append(gp2)
            else: #Mutation 
                child_chromosome.append(self.mutated_genes())
        return Individual(child_chromosome)
    def cal_fitness(self): # Calculating the fitness of each individual.
        w, h = 32, 32
        img = Image.new("RGB", (w, h),"white")
        img1 = ImageDraw.Draw(img,'RGBA') 
        for eachShape in self.chromosome:
            img1.rectangle(eachShape, (105,105,105,125))
        # img.show()
        pix = img.load()
        loss = 0
        originalImage = Image.open('twoSquares.jpg')
        originalPixel = originalImage.load()
        for i in range(0,32):
            for j in range(0,32):
                try:
                    diffRed   = abs(originalPixel[i,j]   - pix[i,j][0]) #Comapring pixel by pixel the RGB values and finding its average
                    diffGreen  = abs(originalPixel[i,j]   - pix[i,j][1])
                    diffBlue  = abs(originalPixel[i,j]   - pix[i,j][2])

                    pctDiffRed   = diffRed / 255 
                    pctDiffGreen = diffGreen / 255
                    pctDiffBlue   = diffBlue  / 255
                    loss = loss + (((pctDiffRed + pctDiffGreen + pctDiffBlue) / 3) * 100) #The sum of difference in each pixel is the fitness of each state
                except:
                    diffRed   = abs(originalPixel[i,j][0]   - pix[i,j][0]) #Some images have RBG as a tuple and some as int. Hence the Try/Except 
                    diffGreen  = abs(originalPixel[i,j][1]   - pix[i,j][1])
                    diffBlue  = abs(originalPixel[i,j][2]   - pix[i,j][2])

                    pctDiffRed   = diffRed / 255 
                    pctDiffGreen = diffGreen / 255
                    pctDiffBlue   = diffBlue  / 255
                    loss = loss + (((pctDiffRed + pctDiffGreen + pctDiffBlue) / 3) * 100)
        return loss

def main():
    global POPULATION_SIZE
    generation = 1
    found = False
    population = []
    for _ in range(POPULATION_SIZE): #Generates the whole population for each generation
        gnome = Individual.create_gnome()
        population.append(Individual(gnome))
    while not found:
        population = sorted(population, key = lambda x:x.fitness) #Arranges the generation in the best fitness order
        print("\n\nLowestLoss: ",population[0].fitness)
        if(generation % 100 == 0 or generation == 1): #Displays the first and every hundredth generation
            w, h = 32, 32
            img = Image.new("RGB", (w, h),"white")
            img1 = ImageDraw.Draw(img,'RGBA') 
            for eachShape in population[0].chromosome: #To draw all the rectanges of the best state in the hundredth generation
                img1.rectangle(eachShape, (105,105,105,125))
            img.show()
        if population[0].fitness <= 15000: #Stops when the difference in pixels in less than or equal to 15000
            found = True
            break
        new_generation = []
        s = int((10*POPULATION_SIZE)/100) #Chooses the top 10% of each population
        new_generation.extend(population[:s])
        s = int((90*POPULATION_SIZE)/100)
        for _ in range(s): #Generates the remaing 90% of the population by randomly mating the 10%
            parent1 = random.choice(population[:50])
            parent2 = random.choice(population[:50])
            count = 0
            
            while((parent2.chromosome == parent1.chromosome) and (count != len(population))):
                parent2 = random.choice(population[:50])
                count = count + 1
            child = parent1.mate(parent2)
            new_generation.append(child)
        
        population = new_generation
        print("Generation: {}\tFitness: {}".format(generation,population[0].fitness))
        generation += 1

    print("Generation: {}\tFitness: {}".format(generation,population[0].fitness))


if __name__ == '__main__':
	main()