#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

#    author: Ali Rasim Kocal <arkocal@gmail.com> - Oct 2017

from itertools import islice
import copy

#TODO decide on best defaults
DEFAULT_NR_OFFSPRINGS = 2
DEFAULT_NR_SURVIVORS = 10

class EvolutinaryParameterOptimizer(object):

    def __init__(self, func,
                 nr_offsprings=DEFAULT_NR_OFFSPRINGS,
                 nr_survivors=DEFAULT_NR_SURVIVORS):
        """
        func: function to optimize

        For nr_offsprings and nr_survivors see variable descriptions
        """
        self.func = func
        self.params_list = []
        """ In each step, the mutate method is called this often
        for each parameter. """
        self.nr_offsprings = nr_offsprings
        """ At the and of each step, the number of parameters is
        reduced to this. """
        self.nr_survivors = nr_survivors


    def mutate(self, *args, **kwargs):
        """
        Override this to implement a fitting mutation
        fitting for the problem.

        This function takes the same parameters as the function being
        optimized and should call the submit_params method with the
        same parameters applied some mutation. For each set of parameters
        this is called nr_survivors times and can call submit_params
        multiple times.
        """
        raise NotImplementedError("This method has to be overloaded.")


    def score(self, result):
        """
        Override this to implement a fitting score function.

        This should return a number.

        result: Result as returned from the function.
        """
        raise NotImplementedError("This method has to be overloaded.")


    def submit_params(self, *args, **kwargs):
        self.params_list.append((args, kwargs))


    def run_step(self):

        def score_func(params):
            """Wrapper function to call self.func and score the result."""
            args, kwargs = params
            result = self.func(*args, **kwargs)
            return self.score(result)

        assert self.params_list, "No parameters found, see submit_params method."

        # Generate new params
        for params in islice(self.params_list, 0, len(self.params_list)):
            for i in range(self.nr_offsprings):
                args, kwargs = copy.deepcopy(params)
                self.mutate(*args, **kwargs)

        # Remove bad evolutions
        self.params_list.sort(key=score_func, reverse=True)
        self.params_list = self.params_list[:self.nr_survivors]

    def get_best(self):
        """ Return the best parameters found yet. """
        return self.params_list[0]
