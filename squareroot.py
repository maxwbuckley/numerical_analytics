#! /usr/bin/python3
"""Iterative method for computing square root based on the Newton technique."""

def _compute_next_iteration(x_previous, a):
  """Computes next approximation x_i in the series
  
  Args:
    x_previous: (float) Previous estimate of x
    a: (float) The value which we want to find the squareroot of.
  Returns:
    (float) The new approximation of x_i.
  """   
  return (1 / 2) * (x_previous + a / x_previous)

def _stop(a, x, max_iterations, iteration):
  """Decide when to stop our iterative method.

  Stops on multiple conditions.

  Args:
    a: (float)
    x: (float)
    max_iterations: (int)
    iteration: (int)

  Returns:
    (bool) if we should stop.
  """
  if iteration > max_iterations: return True
  if abs(a - x**2) < 0.0001: return True
  return False

def square_root(a, max_iterations):
  if a < 0:
    raise ValueError("Can only find the square roots of real numbers.")
  x = a
  iteration = 1
  previous_x = None
  while not _stop(a, x, max_iterations, iteration):
    x = _compute_next_iteration(x, a)
    print(x)
    iteration += 1
  return x

square_root(125348, 20) 

