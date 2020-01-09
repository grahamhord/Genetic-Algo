import random
import matplotlib.pyplot as plt

characters = [' ', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's',
              'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n',
              'm', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S',
              'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N',
              'M', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_',
              '=', '+', '[', ']', '{', '}', ';', "'", ',', '.', '/', ':', '"',
              '<', '>', '?', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
              "'"]


class genesis:
    def __init__(self, target, popsize=200, mutation=5, survivors=50, top=20,):
        """
        On init - creates a population of individuals, sorts them by fitness, and performs run()
        """
        # Exceptions
        if not (popsize >= survivors >= top):
            raise ValueError('top must be subset of survivors. survivors must be subset of popsize.'
                             f'\npopsize = {popsize} \nsurvivors = {survivors} \ntop = {top}')
        if not target:
            raise ValueError('No target provided')

        invalids = set(target) - set(characters)
        if invalids:
            raise ValueError(f'Invalid Characters: {invalids}')

        if popsize < 2 or survivors < 2 or top < 2:
            raise ValueError('popsize, survivors, and top must all be greater than 1.'
                             f'\npopsize = {popsize} \nsurvivors = {survivors} \ntop = {top}')

        # Make sizes all even
        popsize -= popsize % 2
        survivors -= survivors % 2
        top -= top % 2

        # Define terms
        self.popsize = int(popsize)
        self.mutation = int(mutation)
        self.survivors = int(survivors)
        self.top = int(top)
        self.phrase = target
        self.length = len(target)
        # Create a population in self.lst
        self.lst = list()
        while len(self.lst) < self.popsize:
            ind = ''.join([random.choice(characters) for _ in range(self.length)])
            self.lst.append(ind)
        self.lst.sort(key=self.measure, reverse=True)
        self.run()

    def measure(self, ind):
        """
        Measure the fitness of a given individual. Returns fitness score.
        """
        fitness = 0
        for i in range(self.length):
            if (self.phrase[i] == ind[i]):
                fitness += 1
        return fitness

    def mate(self, ind1, ind2):
        # Mutation: pick a number 0-99. If mutation is less than that number, add a random character to baby
        # Genetic Breeding: If no mutation, randomly choose one of the parents characters
        # Add chosen character to baby sequence, repeat until full
        baby = ''
        for i in range(self.length):
            if random.randrange(100) < self.mutation:
                baby += random.choice(characters)
            elif random.randrange(2):
                baby += ind1[i]
            else:
                baby += ind2[i]
        return baby

    def generate(self):
        """
        Plays one round of the game being set up by other parts of the class.
        Rules of Play:
            The population list is pre-sorted based on fitness score
            A high performing portion is kept (n=self.survivors). The rest deleted
            The very top performers (n=self.top) are randomly placed into pairs and bred
            The entire population is then randomly placed into pairs and bred - top performers breed twice
            Breeding stops when population limit is reached
            If everyone breeds before population limit is reached, resort everyone into new pairs and continue
            It is possible to survive the cull and not breed - depending on survivors/popsize

        Returns none. Alters self.lst
        """
        # pop variable lets the function breed only adults from previous
        # generations - no babies
        pop = self.lst[:self.survivors]
        top = self.lst[:self.top]
        self.lst = list(pop)
        # shuffle very top performers and breed together
        random.shuffle(top)
        for i in range(0, len(top), 2):
            if len(self.lst) >= self.popsize:
                break
            self.lst.append(self.mate(top[i], top[i + 1]))
        # shuffle entire population and breed
        # Use a while loop to repeat the process in case newgen is not filled
        # by first pass.
        while len(self.lst) < self.popsize:
            random.shuffle(pop)
            for i in range(0, len(pop), 2):
                if len(self.lst) >= self.popsize:
                    break
                self.lst.append(self.mate(pop[i], pop[i + 1]))
        self.lst.sort(key=self.measure, reverse=True)

    def run(self):
        """
        Runs generation function until the problem is solved
        Reports best performer for first generation and every improvement
        Plots performance over time and summary stats at end of process

        """
       # Set up best, median, worst lists to fill during process and plot at
       # end
        best = [self.measure(self.lst[0])]
        median = [self.measure(self.lst[int(self.popsize / 2)])]
        worst = [self.measure(self.lst[-1])]
        gen = 0
        print(
            f'Generation {gen}: {self.lst[0]} | Score: {self.measure(self.lst[0])}')
        # generate() until problem is solved
        while self.phrase not in self.lst:
            self.generate()
            best.append(self.measure(self.lst[0]))
            median.append(self.measure(self.lst[int(self.popsize / 2)]))
            worst.append(self.measure(self.lst[-1]))
            gen += 1
            if gen > 2 and best[-1] != best[-2]:
                print(f'Generation {gen}: {self.lst[0]} | Score: {best[-1]}')
        self.gen = gen
        self.best = best
        self.median = median
        self.worst = worst
        # Plot performance
        plt.plot(best, label='best')
        plt.plot(median, label='median')
        plt.plot(worst, label='worst')
        plt.xlabel('Generation')
        plt.ylabel('Performance')
        plt.legend()
        plt.show()


genesis('This phrase has 30 characters.')
#genesis('Mutation adds randomness',mutation=15)
# genesis('shortr=fastr')
#genesis('Top performers breed at least twice.',top=30)
#genesis('A larger population is great for working with bigger, more complex problems. More power!!!',popsize=1000,top=200,survivors=400)
