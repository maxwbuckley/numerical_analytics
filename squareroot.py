#! /usr/bin/python3
"""Iterative method for computing square root based on the Newton technique."""

import numpy
import matplotlib
import matplotlib.pyplot as plt
import timeit
import decimal
import pandas
import math

class SquareRootGenerator(object):
  def __init__(self, a, max_iterations, threshold):
    if a < 0:
      raise ValueError("Can only find the square roots of positive real numbers.")
    self.a = a
    self.max_iterations = max_iterations
    # Threshold is defined as the sum of the passed threshold and a multiple
    # of machine epsilon.
    self.threshold = (threshold + 4.0 * numpy.finfo(float).eps * self.a)
    # Need to set initial approximation guess. Using formula from wikipedia
    if a < 10:
      self.approximations = [2 * (10 ** math.floor(math.log(a, 10)/2))]
    else:
      self.approximations = [6 * (10 ** math.floor(math.log(a, 10)/2))]
    self.errors = []
    self._square_root()

  def _compute_next_iteration(self):
    """Computes next approximation x_i in the series
    
    Args:
      x_previous: float previous estimate of x
      a: float The value which we want to find the square root of.
    Returns:
      (float) The new approximation of x_i.
    """   
    return (1 / 2) * (self.approximations[-1] + self.a / self.approximations[-1])


  def _stop(self, iteration):
    """Decide when to stop our iterative method.

    Stops on multiple conditions.

    Args:
      a: float
      x: float
      max_iterations: integer
      iteration: integer

    Returns:
      boolean if we should stop.
    """
    if iteration > self.max_iterations: return True
    # We know the True value desired value so use that for stopping rule.
    error = abs(self.a - self.approximations[-1]**2)
    self.errors.append(error)
    if error < self.threshold: return True
    return False

  def _square_root(self):
    iteration = 1
    while not self._stop(iteration):
      self.approximations.append(self._compute_next_iteration())
      iteration += 1

  def plot_errors(self):
    df = pandas.DataFrame(self.errors)
    df.plot()
    plt.show()

  def plot_approximations(self):
    df = pandas.DataFrame(self.approximations)
    df.plot()
    plt.show()


Generator = SquareRootGenerator(15348, 200, .000000000000000001)
print(Generator.errors)
print(Generator.approximations)
Generator.plot_errors()
Generator.plot_approximations()

