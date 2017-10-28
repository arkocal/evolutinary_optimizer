#
# Example code that starts with a given vector
# and finds a given vector

# To import from parent directory
import sys
sys.path.append('..')

from random import random

from optimizer import EvolutinaryParameterOptimizer

def double_vec(vec):
    return [i*2 for i in vec]


class VectorFinder(EvolutinaryParameterOptimizer):

    def __init__(self, vector_to_find, *args, **kwargs):
        """
        vector_to_find: An iterable containing numbers.
        """
        EvolutinaryParameterOptimizer.__init__(self, *args, **kwargs)
        self.vec = vector_to_find

    def mutate(self, vector):
        for i in range(len(vector)):
            vector[i] += (-0.5 + random())*2
        self.submit_params(vector)

    def score(self, result):
        return -sum([(i-j)**2 for i,j in zip(result, self.vec)])

if __name__=="__main__":
    # Find the vector (3, 4)
    vector_finder = VectorFinder([3,4], double_vec)
    # Feed some initial parameters
    vector_finder.submit_params([0,0])
    vector_finder.submit_params([-4,-2])
    vector_finder.submit_params([2, 7])

    # Run for 1000 steps
    for i in range(1000):
        vector_finder.run_step()

    args, kwargs = vector_finder.get_best()
    # As we have a single argument, we can just print the 0th entry in args
    print("Found:", args[0])
