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
  def __init__(self, a, max_iterations, threshold, is_decimal=False,
               precision=None):
    """Initializes square root generator.

    Args:
      a: The numeric value we want to find the square root of. Must be
          greater than 0.
      max_iterations: The maximum iterations to run for before terminating.
      threshold: the human set precision threshold. Partially overruled by
          machine epsilon to prevent impossible precision requirements.
      is_decimal: boolean of wheter to use decimal.Decimal rather than float.
      precision: integer of how many digits of precision to use.
    Raises:
      ValueError if is_decimal is True without passing a precision value.
      ValueError if passed value of a < 0.
    """
    # Default value
    self.decimal = False
    if is_decimal and not precision:
      raise ValueError("You cannot use decimal without specifying an integer "
                       "precision value") 
    if a < 0:
      raise ValueError("Can only find the square roots of positive real numbers.")
    elif is_decimal:
      self.decimal = True
      self.precision = precision
      decimal.getcontext().prec = self.precision
    if not precision:
      # We are using float.
      precision = 53
    self.a = self.numeric()(a)
    self.max_iterations = max_iterations
    # Threshold is defined as the sum of the passed threshold and a multiple
    # of machine epsilon.
    machine_epsilon = self.numeric()(2) ** -self.numeric()(precision - 1) 
    self.threshold = (
        self.numeric()(threshold) + self.numeric()(4.0) *
        self.numeric()(machine_epsilon) * self.numeric()(
            self.a**self.numeric()(1/2)))
    # Need to set initial approximation guess. Using formula from wikipedia
    if a < 10:
      self.approximations = [self.numeric()(2) * (10 ** math.floor(math.log(a, 10)/2))]
    else:
      self.approximations = [self.numeric()(6) * (10 ** math.floor(math.log(a, 10)/2))]
    self.errors = []
    self._square_root()

  def numeric(self):
    """Returns the numeric type we want for computations.
    
    Either decimal or float depending on the generator settings
    """ 
    if self.decimal: return decimal.Decimal
    return float

  def _compute_next_iteration(self):
    """Computes next approximation x_i in the series
    
    Args:
      x_previous: float previous estimate of x
      a: float The value which we want to find the square root of.
    Returns:
      A float, the new approximation of x_i.
    """   
    return (self.numeric()(1 / 2) * (self.approximations[-1] + 
            self.a / self.approximations[-1]))


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
    error = abs(self.a**self.numeric()(1/2) - self.approximations[-1])
    self.errors.append(error)
    if error < self.threshold: return True
    return False

  def _square_root(self):
    iteration = 1
    while not self._stop(iteration):
      self.approximations.append(self._compute_next_iteration())
      iteration += 1

  def plot_errors(self):
    """Generate a plot of errors."""
    df = pandas.DataFrame({"Errors": [
        float(error) for error in self.errors]})
    df.plot()
    plt.title("Errors from subsequent approximations of square root of %s" %
               self.a)
    plt.ylabel("Absolute error")
    plt.xlabel("Iteration number")
    plt.show()

  def plot_approximations(self):
    """Generate a plot of the sequntial approximations of x_i."""
    df = pandas.DataFrame({"Approximations": [
        float(approximation) for approximation in self.approximations]})
    df.plot()
    plt.title("Approximations of square root of %s" %
               self.a)
    plt.ylabel("Approximation")
    plt.xlabel("Iteration number")
    plt.axhline(self.a**self.numeric()(1/2), color="r")
    plt.show()


if __name__ == '__main__':
  decimal_desired = False
  float_desired = True
  if decimal_desired:
    Generator = SquareRootGenerator(15348, 100, 10**-1000, True, 1024)
    print([(i, error) for i, error in enumerate(Generator.errors)])
    print([(i, error) for i, error in enumerate(Generator.approximations)])
    print(Generator.approximations)
    Generator.plot_errors()
    Generator.plot_approximations()
  if float_desired:
    Generator = SquareRootGenerator(15348, 100, 10**-10)
    print([(i, error) for i, error in enumerate(Generator.errors)])
    print([(i, error) for i, error in enumerate(Generator.approximations)])
    print(Generator.approximations)
    Generator.plot_errors()
    Generator.plot_approximations()

