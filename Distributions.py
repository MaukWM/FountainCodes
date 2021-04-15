import enum
import math

import numpy as np
import random


class Distribution():

    def __init__(self, source_size):
        self.source_size = source_size
        self.probabilities = []

    def sample_from_dist(self):
        raise Exception("Use an implementation")

    def name(self):
        return "no_name_implemented"


class Uniform(Distribution):

    def sample_from_dist(self):
        return random.randint(0, self.source_size - 1)

    def name(self):
        return "Uniform"


class OneShot(Distribution):

    def sample_from_dist(self):
        return 1

    def name(self):
        return "OneShot"


class IdealSoliton(Distribution):

    def __init__(self, source_size):
        super().__init__(source_size)
        # https://en.wikipedia.org/wiki/Soliton_distribution
        self.probabilities.append(1/self.source_size)
        for i in range(2, self.source_size + 1):
            self.probabilities.append(1/(i*(i - 1)))

        print(self.probabilities)
        print(np.sum(self.probabilities))

    def sample_from_dist(self):
        return np.random.choice(np.arange(1, self.source_size + 1), p=self.probabilities)

    def name(self):
        return "IdealSoliton"


class RobustSoliton(Distribution):

    def __init__(self, source_size, c, error_rate):
        super().__init__(source_size)
        # https://en.wikipedia.org/wiki/Soliton_distribution
        self.probabilities.append(1/self.source_size)
        for i in range(2, self.source_size + 1):
            self.probabilities.append(1/(i*(i - 1)))

        if not (c == 0 or error_rate == 0):
            R = c * math.log(source_size / error_rate, math.e) * math.sqrt(source_size)

            # Until (Source size/R) - 1
            for i in range(1, (math.ceil(source_size/R)) - 1):
                # Check if still valid index
                if i < len(self.probabilities):
                    self.probabilities[i - 1] += R / (i * source_size)

            # Source size / R
            if (math.ceil(source_size/R) - 1) < len(self.probabilities):
                self.probabilities[math.ceil(source_size/R) - 1] = ((R * math.log(R / error_rate, math.e)) / source_size)

            self.probabilities = self.probabilities/np.sum(self.probabilities)

        print(self.probabilities)
        print(np.sum(self.probabilities))

    def sample_from_dist(self):
        return np.random.choice(np.arange(1, self.source_size + 1), p=self.probabilities)

    def name(self):
        return "RobustSoliton"

