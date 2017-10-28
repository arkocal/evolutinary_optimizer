# Evolutinary Parameter Optimizer

## How to use

Evolutinary Parameter Optimizer is a framework to find optimal parameters for a function.
Which means you will need a function and a definition of optimal parameters.

Assume we are trying to find the vector closest to `(3,4)` when doubled. Our function is also
scalar multiplying a vector with 2, and our score for each result is the Euclidian distance to
`(3,4)`.

```python
def double_vec(vec):
    # The is the function we are searching the optimal parameters for
    return [i*2 for i in vec]
```

In order to implement the optimizer, we are going to subclass `EvolutinaryParameterOptimizer`.

```python
from optimizer import EvolutinaryParameterOptimizer
# Make sure the optimizer module is on PYTHONPATH

class VectorFinder(EvolutinaryParameterOptimizer):

    def __init__(self, vector_to_find, *args, **kwargs):
       	"""
	vector_to_find: An iterable containing numbers.
	"""
	EvolutinaryParameterOptimizer.__init__(self, *args, **kwargs)
	self.vec = vector_to_find
```

In general, it is not necessary to implement an `__init__` function, but it can be helpful, as in
this example, to keep the optimizer generic. Otherwise we woul have to hard code the vector in the
score function.

The score function of `EvolutinaryParamaterOptimizer` takes a single argument apart from `self`, which is the output of the function.
It returns a number value, representing how good the solution is. In this case it will be -1 * distance
to `(3,4)`. We need the negative because we want to minimize the distance, thus maximize its additional inverse.

```python
def score(self, result):
    return -sum([(i-j)**2 for i,j in zip(result, self.vec)])
```

Finally, we have to override the `mutate` function, which tells how to change the parameters at each
step. This method gets the exact same parameters as the function being optimized, and calls the
`submit` method of `EvolutinaryParameterOptimizer`, which also has the exact same signature. The `submit` method can be called multiple times during `mutate`, but the preferred way is to call it once,
as `mutate` is called multiple times (`EvolutinaryParameterOptimizer.nr_offsprings`).

We will mutate the vector by adding random values to each element. Be sure to call `from random import random` at the beginning of your code.

```python
def mutate(self, vector):
    for i in range(len(vector)):
        vector[i] += (-0.5 + random())*2
    self.submit_params(vector)
```

Finally, in order to run the optimizer, normally `__init__` of `EvolutinaryParameterOptimizer` takes
a single positional argument, the function to optimize, but we have added one more, the vector to find.
After init, we need to submit some initial parameters as starting a starting point, and run a number of
steps.

```python
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
```

The whole functioning example can be found under `examples/example_0_vector.py`